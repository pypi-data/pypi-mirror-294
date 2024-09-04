from .exchange import Exchange
from quantguard.model.balance import Balance
from quantguard.model.position import Position
from quantguard.model.order import Order, DimensionEnum
from quantguard.model.ledger import Ledger, LedgerType
from ccxt import okx
import time
import copy
import logging
import json

logger = logging.getLogger(__name__)


class OKX(Exchange):
    def __init__(self, account_name: str, config: dict):
        super().__init__("okx", account_name, config)
        self.exchange: okx = self.exchange

    def fetch_balance(self, created_at: int) -> Balance:
        ccxt_balance = super().fetch_balance()
        # print(f"account {self.account_name} balance: {ccxt_balance}")
        balance = Balance(
            name=self.account_name,
            exchange=self.exchange_id,
            asset="USDT",
            # total=ccxt_balance["USDT"]["total"],  # 总资产 ，包含了pnl
            total=ccxt_balance["info"]["data"][0]["details"][0]["cashBal"],
            available=ccxt_balance["USDT"]["free"],
            frozen=ccxt_balance["USDT"]["used"],
            borrowed=ccxt_balance["info"]["data"][0]["borrowFroz"],
            ts=ccxt_balance["timestamp"],
            unrealized_pnl=ccxt_balance["info"]["data"][0]["details"][0]["upl"],
            info=json.dumps(ccxt_balance["info"]),
            created_at=created_at,
        )
        return balance

    def fetch_positions(self, created_at: int) -> list[Position]:
        ccxt_position = super()._fetch_positions()
        positions = []
        for pos in ccxt_position:
            # 'symbol': 'DOGE/USDT:USDT'
            base_asset = pos["symbol"].split("/")[0]
            quote_asset = pos["symbol"].split("/")[1].split(":")[0]
            if pos["info"]["instType"] == "SWAP":
                market_type = "UFUTURES"
            else:
                market_type = "SPOT"
            position = Position(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type=market_type,
                base_asset=base_asset,
                quote_asset=quote_asset,
                ts=pos["info"]["cTime"],
                # dimension=pos["side"],
                dimension=DimensionEnum.QUANTITY.value,
                quantity=float(pos["info"]["pos"]) * pos["contractSize"],
                average_price=pos["info"]["avgPx"],
                unrealized_pnl=pos["unrealizedPnl"],
                liquidation_price=(
                    pos["liquidationPrice"] if pos["liquidationPrice"] else ""
                ),
                contract_size=pos["contractSize"],
                info=json.dumps(pos["info"]),
                created_at=created_at,
            )
            positions.append(position)
        return positions

    def parse_operate(self, operate: str, reduceOnly: bool) -> str:
        if reduceOnly:
            return "close"

        if operate == "buy":
            return "open"
        elif operate == "sell":
            return "close"
        return operate

    def fetch_orders_T(self, fetch_orders_T=1) -> list[Order]:
        since = super().get_yesterday_timestamps(fetch_orders_T)
        all_orders = self.loop_fetch_orders(since=since)

        orders = []
        # 一个订单可能对应多个trade, 订单1715876098503593985
        for order in all_orders:
            ccxt_order = self.exchange.parse_order(order)
            if "SWAP" in ccxt_order["symbol"]:
                base_asset = ccxt_order["symbol"].split("-")[0]
                quote_asset = ccxt_order["symbol"].split("-")[1]
            else:
                base_asset = ccxt_order["symbol"].split("/")[0]
                quote_asset = ccxt_order["symbol"].split("/")[1].split(":")[0]

            if ccxt_order["info"]["instType"] == "SWAP":
                market_type = "UFUTURES"
            else:
                market_type = "SPOT"

            contract_size = self.fetch_symbol_contract_size(
                f"{base_asset}/{quote_asset}:{quote_asset}"
            )

            item = Order(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type=market_type,
                base_asset=base_asset,
                quote_asset=quote_asset,
                market_order_id=ccxt_order["id"],
                custom_order_id=(
                    ccxt_order["clientOrderId"]
                    if ccxt_order["clientOrderId"] is not None
                    else ""
                ),
                ts=ccxt_order["timestamp"],
                origin_price=ccxt_order["price"],
                origin_quantity=float(ccxt_order["amount"])
                * contract_size,  # 委托数量, 合约为张数
                total_average_price=ccxt_order["average"],
                total_filled_quantity=float(ccxt_order["filled"])
                * contract_size,  # 成交数量，合约为张数
                # last_average_price=order["info"]["fillPx"],  # 最新成交价格
                # last_filled_quantity=float(order["info"]["fillSz"]) * contract_size,  # 最新成交数量，合约为张数
                order_side=ccxt_order["side"],
                operation=self.parse_operate(
                    ccxt_order["side"], ccxt_order["reduceOnly"]
                ),
                order_time_in_force=(
                    ccxt_order["timeInForce"] if ccxt_order["timeInForce"] else ""
                ),
                reduce_only=True if ccxt_order["reduceOnly"] else False,
                order_type=ccxt_order["type"],
                order_state=ccxt_order["status"],
                dimension=DimensionEnum.QUANTITY.value,
                commission=ccxt_order["fee"]["cost"],
                contract_size=contract_size,
                info=json.dumps(order),
                created_at=int(time.time() * 1000),
            )
            orders.append(item)
        return orders

    def loop_fetch_open_orders(self, since=None):
        all_open_orders = []
        last_id = None
        while True:
            params = {
                "instType": "SWAP",
            }
            if last_id:
                params["before"] = last_id
            open_orders = self.exchange.fetch_open_orders(since=since, params=params)

            if not open_orders:
                break

            last_time = open_orders[-1]["timestamp"]
            all_open_orders += open_orders

            logger.info(
                f"length: {len(open_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}"
            )

            if len(open_orders) < 100 and super().is_cur_day(last_time):
                break

            # 更新 `since` 和 `id`，以便下一轮循环继续获取更早的账单
            last_id = open_orders[-1]["id"]
            time.sleep(0.4)  # 当前接口限制：5次/2秒

        return all_open_orders

    def loop_fetch_closed_orders(self, since=None):
        all_closed_orders = []
        last_id = None
        while True:
            params = {
                "instType": "SWAP",
                "method": "privateGetTradeOrdersHistoryArchive",
            }
            if last_id:
                params["before"] = last_id
            else:
                params["end"] = since
            # TODO 存在第一次取不到数据的情况。 需要 ++1尝试
            closed_orders = self.exchange.fetch_closed_orders(params=params)

            if not closed_orders:
                break

            last_time = closed_orders[-1]["timestamp"]
            all_closed_orders += closed_orders

            logger.info(
                f"length: {len(closed_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}"
            )

            if len(closed_orders) < 100 and super().is_cur_day(last_time):
                break

            # 更新 `since` 和 `id`，以便下一轮循环继续获取更早的账单
            last_id = closed_orders[-1]["id"]
            time.sleep(0.4)  # 当前接口限制：5次/2秒

        return all_closed_orders

    def loop_fetch_orders(self, since=None):
        all_orders = []
        last_id = None
        while True:
            params = {
                "instType": "SWAP",
            }
            if last_id:
                params["before"] = last_id
            else:
                params["end"] = since
            # TODO 存在第一次取不到数据的情况。 需要 ++1尝试
            time.sleep(0.4)  # 当前接口限制：5次/2秒
            resp = self.exchange.private_get_trade_orders_history_archive(params=params)

            orders = resp["data"]
            if len(orders) == 0:
                if not last_id:
                    logger.info(
                        f"no data, since: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
                    )
                    if super().is_cur_day(since):
                        break
                    since += 3600 * 24 * 1000
                    continue
                break
            # 原始数据按时间倒序排列
            last_time = int(orders[0]["cTime"])
            all_orders += orders

            logger.info(
                f"length: {len(orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}"
            )

            if len(orders) < 100 and super().is_cur_day(last_time):
                break

            # 更新 `since` 和 `id`，以便下一轮循环继续获取更早的账单
            last_id = orders[0]["ordId"]

        return all_orders

    def loop_fetch_canceled_orders(self, since=None):
        all_cancel_orders = []
        last_id = None
        while True:
            params = {
                "instType": "SWAP",
                "method": "privateGetTradeOrdersHistoryArchive",
            }
            if last_id:
                params["before"] = last_id
            else:
                params["end"] = since
            # TODO 存在第一次取不到数据的情况。 需要 ++1尝试
            cancel_orders = self.exchange.fetch_canceled_orders(params=params)

            if not cancel_orders:
                break

            last_time = cancel_orders[-1]["timestamp"]
            all_cancel_orders += cancel_orders

            logger.info(
                f"length: {len(cancel_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}"
            )

            if len(cancel_orders) < 100 and super().is_cur_day(last_time):
                break

            # 更新 `since` 和 `id`，以便下一轮循环继续获取更早的账单
            last_id = cancel_orders[-1]["id"]
            time.sleep(0.4)
        return all_cancel_orders

    def fetch_ledgers_T(self, fetch_orders_T=1) -> list[Ledger]:
        ledgers: list[Ledger] = []

        origin_ledgers = self.fetch_origin_ledgers_T(fetch_orders_T)

        for ledger in origin_ledgers:
            ledger_items = self.build_ledger(ledger)
            if ledger_items:
                ledgers += ledger_items

        return ledgers

    def fetch_origin_ledgers_T(self, fetch_orders_T=1):
        since = super().get_yesterday_timestamps(fetch_orders_T)
        last_id = None
        ledgers = []

        while True:
            params = {"instType": "SWAP", "method": "privateGetAccountBillsArchive"}
            # 如果有 `id`，则使用 `before` 参数；否则使用 `end` 参数
            if last_id:
                params["before"] = last_id
            else:
                params["end"] = since
            time.sleep(0.4)  # 当前接口限制：5次/2秒
            ccxt_ledgers = self.exchange.fetch_ledger(params=params)
            if not ccxt_ledgers:
                logger.info(
                    f"okx ledger no data, since: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
                )
                if not last_id:
                    if super().is_cur_day(since):
                        break
                    since += 3600 * 24 * 1000
                    continue
                break

            ledgers += ccxt_ledgers
            last_time = ccxt_ledgers[-1]["timestamp"]

            logger.info(
                f"ledger length: {len(ccxt_ledgers)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}"
            )

            if len(ccxt_ledgers) < 100 and super().is_cur_day(last_time):
                break

            # 更新 `since` 和 `id`，以便下一轮循环继续获取更早的账单
            last_id = ccxt_ledgers[-1]["id"]

        return ledgers

    def build_ledger(self, ledger) -> list[Ledger]:
        # okx的ledger一条记录可能包含  fee, pnl
        ledgers: list[Ledger] = []

        ledger_type = ledger["info"]["type"]
        symbol = ledger["symbol"] if ledger["symbol"] else ""
        if symbol:
            symbol = symbol.replace("/", "-").split(":")[0]

        item = Ledger(
            name=self.account_name,
            exchange=self.exchange_id,
            asset=ledger["currency"],
            symbol=symbol,
            ts=ledger["timestamp"],
            market_type="UFUTURES",
            market_id=ledger["id"],
            trade_id="",
            order_id="",
            ledger_type=ledger_type,
            amount=0,
            info=json.dumps(ledger["info"]),
            created_at=int(time.time() * 1000),
        )
        if ledger_type == "8":  # 资金费率
            fund = copy.deepcopy(item)
            fund.ledger_type = LedgerType.FUNDING_FEE.value
            fund.amount = float(ledger["info"]["pnl"])
            ledgers.append(fund)
            return ledgers

        if ledger_type != "2":  # 忽略掉非交易相关的ledger
            return None

        # 仓位余额, 该数据实际场景中无意思
        # if ledger["info"]["posBalChg"] != "0":
        #     position = copy.deepcopy(item)
        #     position.ledger_type = LedgerType.POSITION_CHANGE.value
        #     position.amount = float(ledger["info"]["posBalChg"]) * -1
        #     ledgers.append(position)

        # 交易手续费
        commission = copy.deepcopy(item)
        commission.ledger_type = LedgerType.COMMISSION_FEE.value
        commission.amount = float(ledger["info"]["fee"])
        commission.trade_id = ledger["info"]["tradeId"]
        commission.order_id = ledger["info"]["ordId"]
        ledgers.append(commission)

        # 买入没有pnl
        if ledger["info"]["subType"] == "1" and float(ledger["info"]["pnl"]) == 0:
            return ledgers

        trade_pnl = copy.deepcopy(item)
        trade_pnl.ledger_type = LedgerType.TRADE_PNL.value
        trade_pnl.amount = float(ledger["info"]["pnl"])
        trade_pnl.trade_id = ledger["info"]["tradeId"]
        trade_pnl.order_id = ledger["info"]["ordId"]
        ledgers.append(trade_pnl)
        return ledgers
