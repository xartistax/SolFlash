import asyncio
import json
from time import sleep
import websockets
from app_config.app_config import AppConfig
from services.env import ConfigENV
from services.logger import setup_logger
from utils.cyan_message import cyan_message
from utils.logSubscribe import process_logSubscribe

logger = setup_logger("WEBSOCKET")


class HeliusWebSocketClient:
    def __init__(
            self,
            socket_id=None,
            socket_url=None,
            socket_method=None,
            socket_params=None
            ):
        
        self.keep_running = True  
        self.socket_id = socket_id
        self.socket_method = socket_method
        self.socket_params = socket_params
        self.socket_url = socket_url

        if not self.socket_url:
            raise ValueError("HELIUS_WSS_URL is not set in AppConfig.ENV")

        logger.info(cyan_message(f"WebSocket URL: {self.socket_url}"))

        self.reconnect_delay = 1  # Initial backoff delay in seconds
        sleep(self.reconnect_delay)  # Wait for the WebSocket to be fully established


    async def connect(self):
        """Connects to the Helius WebSocket and listens for log messages."""
        logger.info(cyan_message("Scanning the blockchain for new coin listings..."))

        while self.keep_running:
            try:
                async with websockets.connect(self.socket_url) as websocket:
                    logger.info(cyan_message("Connected to WebSocket"))
                    print(cyan_message(f"System initialized successfully with Url: {self.socket_url}"))
                    

                    # Reset backoff delay on successful connection
                    self.reconnect_delay = 1  

                    # Send the subscription request
                    await self.subscribe(websocket)

                    # Process incoming messages
                    await self.listen(websocket)


            except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError, TimeoutError) as e:
                if not self.keep_running:
                     break
                logger.warning(f"WebSocket error: {e}. Reconnecting in {self.reconnect_delay} seconds...")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, 60)
                

            except asyncio.CancelledError:
                logger.info("WebSocket listener cancelled. Exiting...")
                break
            except Exception as e:
                logger.error(f"Unexpected WebSocket error: {e}")

            # Exponential backoff with a cap at 60 seconds
            logger.info(f"Reconnecting in {self.reconnect_delay} seconds...")
            await asyncio.sleep(self.reconnect_delay)
            self.reconnect_delay = min(self.reconnect_delay * 2, 60)

    async def subscribe(self, websocket):
        """Sends the subscription request to the WebSocket."""
        subscription_request = {
            "jsonrpc": "2.0",
            "id": self.socket_id,
            "method": self.socket_method,
            "params": self.socket_params
        }
        await websocket.send(json.dumps(subscription_request))
        logger.info(cyan_message("Subscription request sent."))
        cyan_message("Subscription request sent.")

    async def listen(self, websocket):
        """Listens for messages from the WebSocket."""
        async for message in websocket:


            if self.socket_method == "logsSubscribe":
                await process_logSubscribe(message)

            if self.socket_method == "getTokenAccounts":
                print(message)

    async def disconnect(self):
        """Disconnects the WebSocket."""
        logger.info("Disconnecting WebSocket...")
        self.keep_running = False