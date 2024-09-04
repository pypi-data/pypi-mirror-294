from quantguard.dao.clickhouse import ClickHouseConnector
from quantguard.model.order import Order
from clickhouse_driver.errors import Error as ClickhouseError
import logging

loggger = logging.getLogger(__name__)

db = ClickHouseConnector()


class OrderDao:

    @staticmethod
    def insert(order: Order) -> bool:
        query = f"""
            INSERT INTO {Order.__tablename__()}
            (name, exchange, market_type, base_asset, quote_asset, market_order_id, custom_order_id, ts, origin_price, origin_quantity, total_average_price, total_filled_quantity, order_side, operation, order_time_in_force, reduce_only, order_type, order_state, dimension, commission, contract_size, info, created_at)
            VALUES
            """
        params = build_inster_params(order)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert order sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(f"insert order sql: {sql}, an unexpected error occurred: {e}")
        return False

    @staticmethod
    def get_by_market_order_id(market_order_id: str) -> Order:
        query = f"SELECT * FROM {Order.__tablename__()} WHERE market_order_id = '{market_order_id}'"
        result = db.execute(query)
        if result:
            return Order(*result[0])
        return None


def build_inster_params(order: Order) -> str:
    return (
        order.name,
        order.exchange,
        order.market_type,
        order.base_asset,
        order.quote_asset,
        order.market_order_id,
        order.custom_order_id,
        order.ts,
        order.origin_price,
        order.origin_quantity,
        order.total_average_price,
        order.total_filled_quantity,
        order.order_side,
        order.operation,
        order.order_time_in_force,
        order.reduce_only,
        order.order_type,
        order.order_state,
        order.dimension,
        order.commission if order.commission is not None else 0,
        order.contract_size,
        order.info,
        order.created_at,
    )
