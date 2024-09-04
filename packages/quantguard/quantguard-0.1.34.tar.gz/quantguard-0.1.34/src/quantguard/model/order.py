from dataclasses import dataclass, asdict
from enum import Enum


# 交易量维度
class DimensionEnum(Enum):
    LOT = "Lot"  # 张
    QUANTITY = "Quantity"  # 币


@dataclass
class Order:
    name: str  # account_name
    exchange: str  # exchange_id
    market_type: str  # 交易市场类型
    base_asset: str  # 基础资产
    quote_asset: str  # 计价资产
    market_order_id: str  # 交易所订单ID
    custom_order_id: str  # 自定义订单ID
    ts: int  # 下单时间
    origin_price: float  # 下单价格
    origin_quantity: float  # 下单数量
    total_average_price: float  # 总成交均价
    total_filled_quantity: float  # 总成交数量
    operation: str  # 操作 买/卖
    order_side: str  # 订单方向
    order_time_in_force: str  # 订单有效期
    reduce_only: int  # 是否只减仓
    order_type: str  # 订单类型
    order_state: str  # 订单状态
    dimension: DimensionEnum  # 交易量维度
    commission: float  # 手续费
    contract_size: float  # 合约大小
    info: str  # 原始信息
    created_at: int  # 创建时间

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "order"
