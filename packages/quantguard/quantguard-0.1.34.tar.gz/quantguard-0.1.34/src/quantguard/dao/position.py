from quantguard.dao.clickhouse import ClickHouseConnector
from quantguard.model.position import Position
from clickhouse_driver.errors import Error as ClickhouseError
import logging

loggger = logging.getLogger(__name__)

db = ClickHouseConnector()


class PositionDao:

    @staticmethod
    def insert(position: Position) -> bool:
        query = f"""
        INSERT INTO {Position.__tablename__()}
        (name, exchange, market_type, base_asset, quote_asset, ts, dimension, quantity, average_price, unrealized_pnl, liquidation_price, contract_size, info, created_at)
        VALUES
        """
        params = build_inster_params(position)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert position sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"insert position sql: {sql}, an unexpected error occurred: {e}"
            )
        return False

    @staticmethod
    def get_by_name(name: str) -> Position:
        query = f"SELECT * FROM {Position.__tablename__()} FINAL WHERE name = '{name}'"
        result = db.execute(query)
        if result:
            return Position(*result[0])
        return None
    
    @staticmethod
    def get_by_exchange(exchange: str) -> list[Position]:
        query = f"SELECT * FROM {Position.__tablename__()} FINAL WHERE exchange = '{exchange}'"
        result = db.execute(query)
        if result:
            return [Position(*r) for r in result]
        return []

    @staticmethod
    def insert_snapshot(position: Position):
        query = f"""
        INSERT INTO {Position.__snapshot_tablename__()}
        (name, exchange, market_type, base_asset, quote_asset, ts, dimension, quantity, average_price, unrealized_pnl, liquidation_price, contract_size, info, created_at)
        VALUES
        """
        params = build_inster_params(position)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"create_snapshot position sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"create_snapshot position sql: {sql}, an unexpected error occurred: {e}"
            )
        return False


def build_inster_params(position: Position):
    return (
        position.name,
        position.exchange,
        position.market_type,
        position.base_asset,
        position.quote_asset,
        position.ts,
        position.dimension,
        position.quantity,
        position.average_price,
        position.unrealized_pnl,
        position.liquidation_price,
        position.contract_size,
        position.info,
        position.created_at,
    )
