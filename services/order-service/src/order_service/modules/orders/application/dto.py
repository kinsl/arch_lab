from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateOrderDTO:
    user_id: UUID
    product: str
    quantity: int


@dataclass(frozen=True, slots=True)
class UpdateOrderDTO:
    product: str
    quantity: int
