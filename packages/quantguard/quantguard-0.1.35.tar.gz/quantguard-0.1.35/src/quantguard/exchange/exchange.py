import ccxt
from abc import ABC
import datetime
import time
from quantguard.model.ledger import Ledger
from quantguard.model.position import Position


class Exchange(ABC):
    def __init__(self, exchange_id: str, account_name: str, config: dict):
        self.exchange_id = exchange_id
        self.account_name = account_name
        self.exchange: ccxt.Exchange = getattr(ccxt, exchange_id)(config)
        # TODO 基于这个创建不同的客户端
        # self.market_types = ["SPOT", "UFUTURES", "CMFUTURES"]

    def fetch_balance(self, created_at: int = 0, params={}):
        return self.exchange.fetch_balance(params)

    # 获取仓位信息
    def fetch_positions(self, created_at: int = 0) -> list[Position]:
        pass

    def _fetch_positions(self):
        return self.exchange.fetch_positions()

    def get_yesterday_timestamps(self, fetch_orders_T=1):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=fetch_orders_T)
        start_of_yesterday = datetime.datetime(
            yesterday.year, yesterday.month, yesterday.day
        )
        since = int(start_of_yesterday.timestamp() * 1000)
        return since

    # 获取订单信息 T-1
    def fetch_orders_T(self, fetch_orders_T=1):
        since = self.get_yesterday_timestamps(fetch_orders_T)
        return self.exchange.fetch_orders(since=since)

    def fetch_ledgers_T(self, fetch_orders_T=1) -> list[Ledger]:
        pass

    def fetch_symbol_contract_size(self, symbol):
        result = self.exchange.load_markets()
        for key in result.keys():
            if symbol == key:
                # print(f"key {key}, value {result[key]['contractSize']}")
                return result[key]["contractSize"]
        # 张数拿不到，异常处理
        raise Exception(
            f"account: {self.account_name}, exchange: {self.exchange_id}, symbol {symbol} contract size not found"
        )

    def is_cur_day(self, last_time):
        last_date = time.strftime("%Y-%m-%d", time.localtime(last_time / 1000))
        current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        return last_date == current_date
