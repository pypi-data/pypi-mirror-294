from dataclasses import dataclass, asdict
from enum import Enum


# 枚举值
# ledger_type: "funding_fee|transfer_in|transfer_out|deposit|withdraw|deposit_sub|withdraw_sub"
class LedgerType(Enum):
    FUNDING_FEE = "funding_fee"
    TRADE_PNL = "trade_pnl"
    POSITION_CHANGE = "position_change"
    COMMISSION_FEE = "commission_fee"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    DEPOSIT_SUB = "deposit_sub"
    WITHDRAW_SUB = "withdraw_sub"


@dataclass
class Ledger:
    name: str  # 账户名
    exchange: str  # 交易所
    asset: str  # 统计资产币种
    symbol: str  # 交易对
    ts: int  # 时间戳
    market_type: str  # 交易市场类型
    market_id: str  # 交易所ID
    trade_id: str  # 交易ID
    order_id: str  # 订单ID
    ledger_type: LedgerType  # 账目类型
    amount: float  # 金额
    info: str  # 原始信息
    created_at: int  # 创建时间

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "ledger"
