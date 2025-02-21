import asyncio
import signal
from app_config.app_config import AppConfig
from services.api_client import APIClient
from services.logger import setup_logger
from services.env import ConfigENV
from services.websocket import HeliusWebSocketClient
from settings.filters import RUG_CHECKER
from utils.check_rug_pull import check_rug_pull
from utils.handle_shutdown import handle_shutdown  # ✅ Correct import
from utils.setup import setup
from utils.cyan_message import cyan_message

logger = setup_logger("MAIN")



def main():
    if not setup():
        return
    
    logger.info(cyan_message("System initialized successfully!"))
    


    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)


if __name__ == "__main__":
    main()
    client = HeliusWebSocketClient(
        socket_url=ConfigENV.HELIUS_URL,
        socket_method="logsSubscribe", 
        socket_id="fresh-tokens", 
        socket_params=[
            {"mentions": [AppConfig.LIQUIDITY_POOL.get("RADIYUM_PROGRAM_ID")]},
            {"commitment": AppConfig.LIQUIDITY_POOL.get("COMMITMENT")}])


    
    

    asyncio.get_event_loop().run_until_complete(client.connect())

   

    
