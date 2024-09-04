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

logger = logging.getLogger(__name__)


# 交易所账单汇总 worker
class SymmaryWorker(Worker):

    def __init__(self, account: Account):
        super().__init__(account, settings.CRONTABS.BILL_SUMMARY)

    async def run(self):
        logger.info(f"start {self.name} worker")
        await super().run(self.start)

    async def start(self):
        pass
