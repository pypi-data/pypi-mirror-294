"""server"""

import asyncio

from quantguard.config.account import init_account
from quantguard.log.log import init_log
from quantguard.worker.bill_worker import BillWorker
from quantguard.config.account import accounts

import logging

logger = logging.getLogger(__name__)


class Server:

    def __init__(self):
        init_log()
        init_account()

    def run_bill_worker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)  # 设置当前事件循环

        tasks = []
        for account in accounts:
            task = loop.create_task(BillWorker(account=account).run())
            tasks.append(task)
            print(f"create task {account.name}")

        # 等待所有任务完成
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
