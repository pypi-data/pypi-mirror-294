import ccxt
from quantguard.model.balance import Balance
import logging
from quantguard.dao.balance import BalanceDao
from quantguard.dao.position import PositionDao
from quantguard.dao.order import OrderDao
from quantguard.dao.ledger import LedgerDao
import asyncio
from quantguard.config.account import Account
from quantguard.worker.worker import Worker
from quantguard.config import settings
import time
import copy

logger = logging.getLogger(__name__)


# 交易所账单同步 worker
class BillWorker(Worker):

    def __init__(self, account: Account):
        super().__init__(account, settings.CRONTABS.BILL_SYNC)

    async def run(self):
        logger.info(f"start {self.name} worker")
        await super().run(self.start)

    async def start(self):
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.sync())
        created_at = int(time.time() * 1000)
        await asyncio.gather(
            # self.sync_balance(created_at),
            # self.sync_position(created_at),
            # self.sync_order(),
            self.sync_ledger(),
        )

    async def sync_balance(self, created_at: int):
        try:
            balance: Balance = self.exchange.fetch_balance(created_at)
        except ccxt.NetworkError as e:
            logger.warning(f"exchange {self.name} fetch balance network error: {e}")
            return
        except Exception as e:
            logger.warning(f"exchange {self.name} fetch balance exchange error: {e}")
            raise e
        result = BalanceDao().insert(balance)
        logger.info(f"exchange {self.name} balance insert result: {result}")
        result = BalanceDao().insert_snapshot(balance)
        logger.info(f"exchange {self.name} balance snapshot insert result: {result}")
        dao = BalanceDao().get_by_name(self.name)
        if dao:
            logger.info(f"exchange {self.name} from  balance db: {dao.total}")

    async def sync_position(self, created_at: int):
        try:
            positions = self.exchange.fetch_positions(created_at)
        except ccxt.NetworkError as e:
            logger.warning(f"exchange {self.name} fetch position network error: {e}")
            return
        except Exception as e:
            logger.warning(f"exchange {self.name} fetch position exchange error: {e}")
            raise e

        new_position_base_asset = []
        for position in positions:
            result = PositionDao().insert(position)
            logger.info(f"exchange {self.name} position insert result: {result}")
            result = PositionDao().insert_snapshot(position)
            logger.info(
                f"exchange {self.name} position snapshot insert result: {result}"
            )
            new_position_base_asset.append(position.base_asset)
        # db获取持仓信息
        # db存在，positions不存在则删除，snapshot数据新增一条0数据.
        db_positions = PositionDao().get_by_exchange(self.account.exchange.lower())
        for db_position in db_positions:
            if (
                db_position.quantity != 0
                and db_position.base_asset not in new_position_base_asset
            ):
                item = copy.deepcopy(db_position)
                item.quantity = 0
                item.created_at = (
                    positions[0].created_at
                    if len(positions) > 0
                    else int(time.time() * 1000)
                )
                item.liquidation_price = (
                    item.liquidation_price if item.liquidation_price else ""
                )
                result = PositionDao().insert(item)
                logger.info(
                    f"exchange {self.name} position inset zero result: {result}"
                )
                result = PositionDao().insert_snapshot(item)
                logger.info(
                    f"exchange {self.name} position snapshot inset zero result: {result}"
                )

    async def sync_order(self):
        try:
            orders = self.exchange.fetch_orders_T(settings.BILL_SYNC.ORDER_DAYS)
        except ccxt.NetworkError as e:
            logger.warning(f"exchange {self.name} fetch order network error: {e}")
            return
        except Exception as e:
            logger.warning(f"exchange {self.name} fetch order exchange error: {e}")
            raise e
        already_exists = 0
        for order in orders:
            result = OrderDao().get_by_market_order_id(order.market_order_id)
            if result:
                already_exists += 1
                continue
            result = OrderDao().insert(order)
            logger.info(f"exchange {self.name} order insert result: {result}")
        logger.info(
            f"exchange {self.name} order already exists: {already_exists} / {len(orders)}"
        )

    async def sync_ledger(self):
        try:
            ledgers = self.exchange.fetch_ledgers_T(settings.BILL_SYNC.LEDGER_DAYS)
        except ccxt.NetworkError as e:
            logger.warning(f"exchange {self.name} fetch ledger network error: {e}")
            return
        except Exception as e:
            logger.warning(f"exchange {self.name} fetch ledger exchange error: {e}")
            raise e
        already_exists = 0
        for ledger in ledgers:
            if ledger.ledger_type == "position_change":
                print(ledger.to_dict())
            result = LedgerDao().get_by_market_id(ledger.market_id, ledger.ledger_type)
            if result:
                already_exists += 1
                continue
            result = LedgerDao().insert(ledger)
            logger.info(f"exchange {self.name} ledger insert result: {result}")
        logger.info(
            f"exchange {self.name} ledger already exists: {already_exists} / {len(ledgers)}"
        )
