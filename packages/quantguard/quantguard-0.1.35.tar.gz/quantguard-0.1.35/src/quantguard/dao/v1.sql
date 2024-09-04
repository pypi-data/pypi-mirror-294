TRUNCATE TABLE balance;
TRUNCATE TABLE balance_snapshot;
TRUNCATE TABLE position;
TRUNCATE TABLE position_snapshot;
TRUNCATE TABLE order;
TRUNCATE TABLE ledger;


-- 创建新表 balance
CREATE TABLE balance
(
    `name` String NOT NULL COMMENT '用户账户名',
    `exchange` String NOT NULL COMMENT '交易所',
    `asset` String NOT NULL COMMENT '资产名称',
    `total` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '总余额',
    `available` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '可用余额',
    `frozen` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '冻结余额',
    `borrowed` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '借贷金额',
    `unrealized_pnl` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '未实现盈亏',
    `ts` SimpleAggregateFunction(anyLast, Nullable(UInt64)) DEFAULT NULL COMMENT '时间戳',
    `info` SimpleAggregateFunction(anyLast, Nullable(String)) DEFAULT NULL COMMENT '原始信息',
    `created_at` SimpleAggregateFunction(anyLast, Nullable(UInt64)) DEFAULT NULL COMMENT '创建时间'
) ENGINE = AggregatingMergeTree()
ORDER BY (name, exchange, asset) 
COMMENT '资产表';


-- 创建新表 balance_snapshot
CREATE TABLE balance_snapshot
(
    `name` String NOT NULL COMMENT '用户账户名',
    `exchange` String NOT NULL COMMENT '交易所',
    `asset` String NOT NULL COMMENT '资产名称',
    `total` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '总余额',
    `available` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '可用余额',
    `frozen` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '冻结余额',
    `borrowed` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '借贷金额',
    `unrealized_pnl` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '未实现盈亏',
    `ts` SimpleAggregateFunction(anyLast, Nullable(UInt64)) DEFAULT NULL COMMENT '时间戳',
    `info` SimpleAggregateFunction(anyLast, Nullable(String)) DEFAULT NULL COMMENT '原始信息',
    `created_at` UInt64 NOT NULL COMMENT '创建时间'
) ENGINE = AggregatingMergeTree()
ORDER BY (name, exchange, asset, created_at) 
COMMENT '资产快照表';

CREATE TABLE position
(
    `name` String NOT NULL COMMENT '用户账户名',
    `exchange` String NOT NULL COMMENT '交易所',
    `market_type` String NOT NULL COMMENT '交易市场类型',
    `base_asset` String NOT NULL COMMENT '基础资产',
    `quote_asset` String NOT NULL COMMENT '计价资产',
    `ts`  SimpleAggregateFunction(anyLast, Nullable(UInt64)) DEFAULT NULL COMMENT '开仓时间',
    `dimension` String  DEFAULT NULL COMMENT '仓位方向',
    `quantity` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '仓位数量',
    `average_price` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '开仓均价',
    `unrealized_pnl` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '未实现盈亏',
    `liquidation_price` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '爆仓价格',
    `contract_size` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '合约大小',
    `info` SimpleAggregateFunction(anyLast, Nullable(String)) DEFAULT NULL COMMENT '原始信息',
    `created_at`  SimpleAggregateFunction(anyLast, Nullable(UInt64)) DEFAULT NULL COMMENT '创建时间'
) ENGINE = AggregatingMergeTree()
ORDER BY (name, exchange, base_asset, quote_asset)
COMMENT '仓位表';

CREATE TABLE position_snapshot
(
    `name` String NOT NULL COMMENT '用户账户名',
    `exchange` String NOT NULL COMMENT '交易所',
    `market_type` String NOT NULL COMMENT '交易市场类型',
    `base_asset` String NOT NULL COMMENT '基础资产',
    `quote_asset` String NOT NULL COMMENT '计价资产',
    `ts` SimpleAggregateFunction(anyLast, Nullable(UInt64))  DEFAULT NULL COMMENT '开仓时间',
    `dimension` String  DEFAULT NULL COMMENT '仓位方向',
    `quantity` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '仓位数量',
    `average_price` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '开仓均价',
    `unrealized_pnl` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '未实现盈亏',
    `liquidation_price` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '爆仓价格',
    `contract_size` SimpleAggregateFunction(anyLast, Nullable(Float64)) DEFAULT NULL COMMENT '合约大小',
    `info` SimpleAggregateFunction(anyLast, Nullable(String)) DEFAULT NULL COMMENT '原始信息',
    `created_at` UInt64 NOT NULL COMMENT '创建时间'
) ENGINE = AggregatingMergeTree()
ORDER BY (name, exchange, base_asset, quote_asset, created_at)
COMMENT '仓位快照表';


CREATE TABLE order
(
    `name` String NOT NULL COMMENT '用户账户名',
    `exchange` String NOT NULL COMMENT '交易所',
    `market_type` String NOT NULL COMMENT '交易市场类型',
    `base_asset` String NOT NULL COMMENT '基础资产',
    `quote_asset` String NOT NULL COMMENT '计价资产',
    `market_order_id` String NOT NULL COMMENT '交易所订单ID',
    `custom_order_id` String NOT NULL COMMENT '自定义订单ID',
    `ts` UInt64 NOT NULL COMMENT '下单时间',
    `origin_price` Float64 DEFAULT NULL COMMENT '下单价格',
    `origin_quantity` Float64 DEFAULT NULL COMMENT '下单数量',
    `total_average_price` Float64 DEFAULT NULL COMMENT '总成交均价',
    `total_filled_quantity` Float64 DEFAULT NULL COMMENT '总成交数量',
    `order_side` String NOT NULL COMMENT '订单方向',
    `operation` String NOT NULL COMMENT '操作类型 open/close',      
    `order_time_in_force` String DEFAULT NULL COMMENT '订单有效期',
    `reduce_only` UInt8 NOT NULL COMMENT '是否只减仓',
    `order_type` String NOT NULL COMMENT '订单类型',
    `order_state` String DEFAULT NULL COMMENT '订单状态',
    `dimension` String DEFAULT NULL COMMENT '仓位方向',
    `commission` Float64 DEFAULT NULL COMMENT '手续费',
    `contract_size` Float64 DEFAULT NULL COMMENT '合约大小',
    `info` String DEFAULT NULL COMMENT '原始信息',
    `created_at` UInt64 NOT NULL COMMENT '创建时间'
) ENGINE = MergeTree()
ORDER BY (market_order_id)
COMMENT '订单表';

CREATE TABLE ledger
(
    `name` String NOT NULL COMMENT '用户账户名',
    `exchange` String NOT NULL COMMENT '交易所',
    `asset` String DEFAULT NULL COMMENT '资产名称',
    `symbol` String DEFAULT NULL COMMENT '交易对',
    `ts` UInt64 NOT NULL COMMENT '时间戳',
    `market_type` String NOT NULL COMMENT '交易市场类型',
    `market_id` String NOT NULL COMMENT '交易所ID',
    `trade_id` String DEFAULT NULL COMMENT '交易ID',
    `order_id` String DEFAULT NULL COMMENT '订单ID',
    `ledger_type` String NOT NULL COMMENT '账目类型',
    `amount` Float64 DEFAULT NULL COMMENT '金额',
    `info` String DEFAULT NULL COMMENT '原始信息',
    `created_at` UInt64 NOT NULL COMMENT '创建时间'
) ENGINE = MergeTree()
ORDER BY (market_id, ledger_type)
COMMENT '账目表';