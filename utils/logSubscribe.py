import asyncio
import json

from services.logger import setup_logger
from utils.handle_shutdown import handle_shutdown
from utils.cyan_message import cyan_message
from utils.handle_transactions import handle_transaction


async def process_logSubscribe(message):
    logger = setup_logger("WEBSOCKET")
    try:
        parsed = json.loads(message)

        if "result" in parsed and not parsed.get("error"):
            logger.info(cyan_message("Subscription confirmed."))
            print(cyan_message("Subscription confirmed."))


        if parsed.get("error"):
            logger.error(f"RPC Error: {parsed['error']}")
            return


        val = parsed.get("params", {}).get("result", {}).get("value", {})
        logs = val.get("logs", [])
        signature = val.get("signature", "")

        if not logs or not signature:
            logger.warning("No logs or signature found in message.")
            return


        # Process transaction asynchronously
        await handle_transaction(signature)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode message: {e}")
        handle_shutdown()
    except Exception as e:
        logger.error(f"Unexpected error in message processing: {e}")
        handle_shutdown()