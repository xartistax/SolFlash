import os
import time
import threading
import requests
from requests.exceptions import RequestException
from app_config.app_config import AppConfig
from services.logger import setup_logger

logger = setup_logger("API CLIENT")


class APIClient:
    def __init__(self, rate_limit: int = 10, time_window: int = 60, max_retries: int = 3):
        """
        Initialize the APIClient.

        :param rate_limit: Maximum number of requests allowed in the time window.
        :param time_window: Time window in seconds for the rate limit.
        :param max_retries: Maximum number of retries for failed requests.
        """
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.max_retries = max_retries
        self.request_times = []  # Track timestamps of recent requests
        self.headers = {"User-Agent": "MyAPIClient/1.0"}
        self.timeout = AppConfig.APICLIENT["TIMEOUT"] / 1000
        self.lock = threading.Lock()  # Lock for thread safety




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
        """Perform a GET request with rate limiting and retry logic."""
        retries = 0
        while retries <= self.max_retries:
            try:
                # Enforce rate limit before making the request
                self._check_rate_limit()

                # Make the request
                response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
                response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

                # Record the request timestamp
                with self.lock:
                    self.request_times.append(time.time())

                # Return both JSON data and status code
                return response.json(), response.status_code

            except (requests.HTTPError, RequestException) as e:
                # Get the status code if available
                status_code = response.status_code if response else None

                if status_code == 429 or (status_code and 500 <= status_code < 600):
                    # Retry for 429 or 5xx errors
                    retries += 1
                    if retries <= self.max_retries:
                        # Exponential backoff: sleep for 2^retries seconds, capped at 30 seconds
                        sleep_time = min(AppConfig.APICLIENT.get("RETRY_DELAY") / 1000 * (2 ** retries), 30)
                        logger.warning(f"Retry {retries}/{self.max_retries} for URL: {url}. Error: {e}. Sleeping for {sleep_time} seconds...")
                        time.sleep(sleep_time)
                    else:
                        logger.error(f"Max retries exceeded for URL: {url}. Error: {e}")
                        return None, status_code
                else:
                    # Non-retryable error
                    logger.error(f"Error occurred for URL {url}: {e}")
                    return None, status_code

        # If all retries fail, return None, None
        return None, None

    def _check_rate_limit(self):
        """Check if the rate limit has been exceeded and sleep if necessary."""
        with self.lock:
            now = time.time()
            # Remove timestamps older than the current time window
            self.request_times = [t for t in self.request_times if now - t < self.time_window]

            if len(self.request_times) >= self.rate_limit:
                # Rate limit exceeded, sleep until the oldest request is outside the time window
                sleep_time = self.time_window - (now - self.request_times[0])
                logger.warning(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                # Update the request timestamps after sleeping
                self.request_times = [t for t in self.request_times if now + sleep_time - t < self.time_window]