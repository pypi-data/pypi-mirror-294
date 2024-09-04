import logging
from croniter import croniter
import asyncio
from quantguard.config.account import Account
from quantguard.exchange.exchange import Exchange
from quantguard.config import settings
import time

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, account: Account, cron_config: str):
        self.name = account.name
        self.account: Account = account
        self.exchange: Exchange = self.create_exchange(account)
        # 定义 cron 表达式，例如 "10 * * * *" 表示每小时的第 10 分钟执行
        self.cron = croniter(cron_config, time.time())

    def create_exchange(self, account: Account) -> Exchange:
        config = {
            "apiKey": account.access_key,
            "secret": account.secret_key,
            "enableRateLimit": True,
        }
        # # 如果设置了代理，添加到配置中
        if settings.PROXY_URL:
            config["proxies"] = {
                "http": settings.PROXY_URL,
                "https": settings.PROXY_URL,
            }

        # 目前可能只有okx需要
        if account.passphrase:
            config["password"] = account.passphrase

        # #TODO 当前暂时只支持swap， 可能需要提供一个需要配置defaultType的交易所
        if account.exchange == "OKX" and "UFUTURES" in account.markets:
            config["options"] = {
                "defaultType": "UFUTURES",
            }

        if account.exchange == "OKX":
            from quantguard.exchange.okx import OKX

            return OKX(account.name, config)
        elif account.exchange == "GATE":
            from quantguard.exchange.gate import GATE

            return GATE(account.name, config)

    async def run(self, func: callable):
        # while True:
        #     diff_time = self.cron.get_next() - time.time()
        #     await asyncio.sleep(diff_time)
        #     await func()
        await func()
