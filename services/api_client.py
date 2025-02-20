import time
import threading
import requests
from requests.exceptions import RequestException
from app_config.app_config import AppConfig
from services.logger import setup_logger

logger = setup_logger("API CLIENT")


class APIClient:
    
    def __init__(self, rate_limit: int = 10, time_window: int = 60, max_retries: int = 3, cache_ttl: int = 300):
        """
        Initialize the APIClient.

        :param rate_limit: Maximum number of requests allowed in the time window.
        :param time_window: Time window in seconds for the rate limit.
        :param max_retries: Maximum number of retries for failed requests.
        :param cache_ttl: Time-to-live (TTL) for cached responses in seconds.
        """
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.max_retries = max_retries
        self.cache_ttl = cache_ttl
        self.request_times = []  # Track timestamps of recent requests
        self.headers = {"User-Agent": "MyAPIClient/1.0"}
        self.timeout = AppConfig.APICLIENT["TIMEOUT"] / 1000
        self.lock = threading.Lock()  # Lock for thread safety

        # In-memory cache: {url+sorted(params): (response, expiration_time)}
        self.cache = {}

    def post(self, url: str, data: dict = None):
        """Perform a POST request."""
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
        return None, None

    def get(self, url: str, params: dict = None):
        """Perform a GET request with caching, rate limiting, and retry logic."""
        cache_key = self._generate_cache_key(url, params)

        # Check cache before making a request
        with self.lock:
            if cache_key in self.cache:
                response, expiry = self.cache[cache_key]
                if time.time() < expiry:
                    logger.info(f"Cache hit for {url} with params {params}")
                    return response, 200  # Cached response with HTTP 200 status
                else:
                    logger.info(f"Cache expired for {url}. Fetching fresh data.")
                    del self.cache[cache_key]  # Remove expired cache

        retries = 0
        while retries <= self.max_retries:
            try:
                # Enforce rate limit before making the request
                self._check_rate_limit()

                # Make the request
                response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
                response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

                json_response = response.json()

                # Store response in cache
                with self.lock:
                    self.cache[cache_key] = (json_response, time.time() + self.cache_ttl)

                # Record the request timestamp
                with self.lock:
                    self.request_times.append(time.time())

                return json_response, response.status_code

            except (requests.HTTPError, RequestException) as e:
                status_code = response.status_code if response else None

                if status_code == 429 or (status_code and 500 <= status_code < 600):
                    retries += 1
                    if retries <= self.max_retries:
                        sleep_time = min(AppConfig.APICLIENT.get("RETRY_DELAY") / 1000 * (2 ** retries), 30)
                        logger.warning(f"Retry {retries}/{self.max_retries} for URL: {url}. Error: {e}. Sleeping for {sleep_time} seconds...")
                        time.sleep(sleep_time)
                    else:
                        logger.error(f"Max retries exceeded for URL: {url}. Error: {e}")
                        return None, status_code
                else:
                    logger.error(f"Error occurred for URL {url}: {e}")
                    return None, status_code

        return None, None

    def _generate_cache_key(self, url: str, params: dict):
        """Generate a cache key using the URL and sorted parameters."""
        params_str = "&".join(f"{key}={value}" for key, value in sorted(params.items())) if params else ""
        return f"{url}?{params_str}"

    def _check_rate_limit(self):
        """Check if the rate limit has been exceeded and sleep if necessary."""
        with self.lock:
            now = time.time()
            self.request_times = [t for t in self.request_times if now - t < self.time_window]

            if len(self.request_times) >= self.rate_limit:
                sleep_time = self.time_window - (now - self.request_times[0])
                logger.warning(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                self.request_times = [t for t in self.request_times if now + sleep_time - t < self.time_window]
