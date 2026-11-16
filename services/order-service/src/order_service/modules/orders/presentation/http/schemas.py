from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from order_service.modules.orders.application.dto import CreateOrderDTO, UpdateOrderDTO
from order_service.modules.orders.domain.notification_status import NotificationStatus

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)]


class CreateOrderBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: UUID
    product: Text
    quantity: Annotated[int, Field(strict=True, ge=1, le=10000)]

    def to_dto(self) -> CreateOrderDTO:
        return CreateOrderDTO(user_id=self.user_id, product=self.product, quantity=self.quantity)


class UpdateOrderBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product: Text
    quantity: Annotated[int, Field(strict=True, ge=1, le=10000)]

    def to_dto(self) -> UpdateOrderDTO:
        return UpdateOrderDTO(product=self.product, quantity=self.quantity)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    product: str
    quantity: int
    email: str
    notification_status: NotificationStatus
