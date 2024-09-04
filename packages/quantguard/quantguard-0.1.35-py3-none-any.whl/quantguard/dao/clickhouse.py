from quantguard.config import settings
from clickhouse_driver import Client, connect


class ClickHouseConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self._client = Client(
            host=settings.CLICKHOUSE.HOST,
            port=settings.CLICKHOUSE.PORT,
            user=settings.CLICKHOUSE.USERNAME,
            password=settings.CLICKHOUSE.PASSWORD,
            database=settings.CLICKHOUSE.DATABASE,
        )

        self._connection = connect(
            host=settings.CLICKHOUSE.HOST,
            port=settings.CLICKHOUSE.PORT,
            user=settings.CLICKHOUSE.USERNAME,
            password=settings.CLICKHOUSE.PASSWORD,
            database=settings.CLICKHOUSE.DATABASE,
        )

    def execute(self, query):
        return self._client.execute(query)

    def close(self):
        self._client.disconnect()

    def get_connection(self):
        return self._connection
