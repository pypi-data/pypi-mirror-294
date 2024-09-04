from dataclasses import dataclass, asdict


@dataclass
class Position:
    name: str  # 账户名
    exchange: str  # 交易所
    market_type: str  # 交易市场类型
    base_asset: str  # 基础资产
    quote_asset: str  # 计价资产
    ts: int  # 开仓时间
    dimension: str  # 仓位方向
    quantity: float  # 仓位数量
    average_price: float  # 开仓均价
    unrealized_pnl: float  # 未实现盈亏 TODO 不需要记录已实现盈亏？
    liquidation_price: float  # 爆仓价格
    contract_size: float  # 合约大小
    info: str
    created_at: int  # 创建时间

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "position"

    @classmethod
    def __snapshot_tablename__(self):
        return "position_snapshot"
