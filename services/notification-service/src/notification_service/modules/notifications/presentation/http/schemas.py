from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

from notification_service.modules.notifications.application.dto import CreateNotificationDTO, UpdateNotificationDTO

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)]


class CreateNotificationBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_id: UUID
    email: EmailStr
    message: Text

    def to_dto(self) -> CreateNotificationDTO:
        return CreateNotificationDTO(order_id=self.order_id, email=str(self.email), message=self.message)


class UpdateNotificationBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    message: Text

    def to_dto(self) -> UpdateNotificationDTO:
        return UpdateNotificationDTO(email=str(self.email), message=self.message)


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    order_id: UUID
    email: str
    message: str
