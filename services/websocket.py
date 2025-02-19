import asyncio
import json
import websockets
from app_config.app_config import AppConfig
from services.env import ConfigENV
from services.logger import setup_logger
from utils import handle_shutdown
from utils.cyan_message import cyan_message
from utils.handle_transactions import handle_transaction

logger = setup_logger("WEBSOCKET")


class HeliusWebSocketClient:
    def __init__(self):
        self.api_url = ConfigENV.HELIUS_URL  
        if not self.api_url:
            raise ValueError("HELIUS_WSS_URL is not set in AppConfig.ENV")

        self.raydium_id = AppConfig.LIQUIDITY_POOL.get("RADIYUM_PROGRAM_ID")
        self.commitment = AppConfig.LIQUIDITY_POOL.get("COMMITMENT")

        if not self.raydium_id or not self.commitment:
            raise ValueError("Liquidity pool ID or commitment is not set in AppConfig.LIQUIDITY_POOL")

        logger.info(cyan_message(f"WebSocket URL: {self.api_url}"))
        self.reconnect_delay = 1  # Initial backoff delay in seconds

    async def connect(self):
        """Connects to the Helius WebSocket and listens for log messages."""
        logger.info(cyan_message("Scanning the blockchain for new coin listings..."))

        while True:
            try:
                async with websockets.connect(self.api_url) as websocket:
                    logger.info(cyan_message("Connected to WebSocket"))
                    print(cyan_message("System initialized successfully!"))
                    

                    # Reset backoff delay on successful connection
                    self.reconnect_delay = 1  

                    # Send the subscription request
                    await self.subscribe(websocket)

                    # Process incoming messages
                    await self.listen(websocket)

            except websockets.exceptions.ConnectionClosedError as e:
                logger.warning(f"WebSocket closed: {e}. Reconnecting...")
            except (ConnectionRefusedError, TimeoutError) as e:
                logger.error(f"Connection error: {e}. Retrying...")
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
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {"mentions": [self.raydium_id]},
                {"commitment": self.commitment}
            ]
        }
        await websocket.send(json.dumps(subscription_request))
        logger.info(cyan_message("Subscription request sent."))
        cyan_message("SSubscription request sent.")

    async def listen(self, websocket):
        """Listens for messages from the WebSocket."""
        async for message in websocket:
            try:
                parsed = json.loads(message)

                if "result" in parsed and not parsed.get("error"):
                    logger.info(cyan_message("Subscription confirmed."))
                    print(cyan_message("Subscription confirmed."))
                    continue

                if parsed.get("error"):
                    logger.error(f"RPC Error: {parsed['error']}")
                    continue

                val = parsed.get("params", {}).get("result", {}).get("value", {})
                logs = val.get("logs", [])
                signature = val.get("signature", "")

                if not logs or not signature:
                    logger.warning("No logs or signature found in message.")
                    continue

                # Process transaction asynchronously
                asyncio.create_task(handle_transaction(signature))

            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode message: {e}")
                handle_shutdown()
            except Exception as e:
                logger.error(f"Unexpected error in message processing: {e}")
                handle_shutdown()

