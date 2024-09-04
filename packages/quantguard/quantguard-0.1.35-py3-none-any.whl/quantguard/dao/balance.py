from quantguard.dao.clickhouse import ClickHouseConnector
from quantguard.model.balance import Balance
from clickhouse_driver.errors import Error as ClickhouseError
import logging

loggger = logging.getLogger(__name__)

db = ClickHouseConnector()


class BalanceDao:
    @staticmethod
    def insert(balance: Balance) -> bool:
        query = f"""
        INSERT INTO {Balance.__tablename__()}
        (name, exchange, asset, total, available, frozen, borrowed, unrealized_pnl, ts, info, created_at)
        VALUES
        """
        params = build_inster_params(balance=balance)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert balance sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"insert balance sql: {sql}, an unexpected error occurred: {e}"
            )
        return False

    @staticmethod
    def get_by_name(name: str) -> Balance:
        query = f"SELECT * FROM {Balance.__tablename__()} FINAL WHERE name = '{name}'"
        result = db.execute(query)
        if result:
            return Balance(*result[0])
        return None

    @staticmethod
    def insert_snapshot(balance: Balance):
        query = f"""
        INSERT INTO {Balance.__snapshot_tablename__()}
        (name, exchange, asset, total, available, frozen, borrowed, unrealized_pnl, ts, info, created_at)
        VALUES
        """
        params = build_inster_params(balance=balance)
        sql = f"{query} {params}"
        try:
            db.execute(sql)
            return True
        except ClickhouseError as e:
            logging.error(f"insert snapshot balance sql: {sql}, error: {e}")
        except Exception as e:
            logging.error(
                f"insert snapshot balance sql: {sql}, an unexpected error occurred: {e}"
            )
        return False

    @staticmethod
    def get_snapshot_by_name(name: str) -> Balance:
        query = f"SELECT * FROM {Balance.__snapshot_tablename__()} WHERE name = %(name)s FINAL"
        result = ClickHouseConnector.execute(query, {"name": name})
        if result:
            return Balance(*result[0])
        return None

    @staticmethod
    def get_snapshot_by_name_and_ts(name: str, since: int) -> list[Balance]:
        query = f"SELECT * FROM {Balance.__snapshot_tablename__()} WHERE name = %(name)s AND ts >= %(ts)s FINAL"
        result = ClickHouseConnector.execute(query, {"name": name, "ts": since})
        return [Balance(*row) for row in result]


def build_inster_params(balance: Balance):
    return (
        balance.name,
        balance.exchange,
        balance.asset,
        balance.total,
        balance.available,
        balance.frozen,
        balance.borrowed,
        balance.unrealized_pnl,
        balance.ts,
        balance.info,
        balance.created_at,
    )
