from dataclasses import dataclass, asdict


@dataclass
class Balance:
    name: str
    exchange: str
    asset: str
    total: float
    available: float
    frozen: float
    borrowed: float
    unrealized_pnl: float
    ts: int
    info: str
    created_at: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def __tablename__(self):
        return "balance"

    @classmethod
    def __snapshot_tablename__(self):
        return "balance_snapshot"
