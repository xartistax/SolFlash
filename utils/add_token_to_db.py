from app_config.app_config import AppConfig
from services.database import PostgresDB
from services.env import ConfigENV
from services.logger import setup_logger


logger = setup_logger("RUGCHECK")


def add_token_to_db(coin_data):
    db = db_connect()
    creating_table(db)
    save_coin(db, coin_data)
    db.close()


def db_connect():
    host = ConfigENV.ENV.get("PGHOST")
    db = ConfigENV.ENV.get("PGDATABASE")
    password = ConfigENV.ENV.get("PGPASSWORD")
    user = ConfigENV.ENV.get("PGUSER")

    db = PostgresDB(host=host , database=db, user=user, password=password)
    db.connect()

    return db


def creating_table(db):
    # Define columns for the table
    columns = {
        "id": "SERIAL PRIMARY KEY",
        "address": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "symbol": "TEXT NOT NULL",
        "price_usd": "DECIMAL(18, 10)",
        "market_cap": "DECIMAL(18, 2)",
        "volume_5m": "DECIMAL(18, 2)",
        "liquidity_usd": "DECIMAL(18, 2)",
        "fdv": "DECIMAL(18, 6)",
        "price_change_5m": "DECIMAL(18, 2)",
        "txn_buy_5min": "INT",
        "txn_sell_5min": "INT",
        "url": "TEXT NOT NULL",
        "social_links": "TEXT NOT NULL",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }
    
    # Create the table if it doesn't already exist
    db.create_table(AppConfig.DB_TRADE_TABLE, columns)







def save_coin(db, coin_data):
    query = f"""
    INSERT INTO {AppConfig.DB_TRADE_TABLE} (address, name, symbol, price_usd, market_cap, volume_5m, liquidity_usd, fdv, price_change_5m, txn_buy_5min, txn_sell_5min, url, social_links)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        coin_data["address"],
        coin_data["name"],
        coin_data["symbol"],
        coin_data["price_usd"],
        coin_data["market_cap"],
        coin_data["volume_5m"],
        coin_data["liquidity_usd"],
        coin_data["fdv"],
        coin_data["price_change_5m"],
        coin_data["txn_buy_5min"],
        coin_data["txn_sell_5min"],
        coin_data["url"],
        coin_data["social_links"],
    )
    
    db.execute_update(query, values)

    logger.warning(f"Coin {coin_data['name']} added to the database.")

