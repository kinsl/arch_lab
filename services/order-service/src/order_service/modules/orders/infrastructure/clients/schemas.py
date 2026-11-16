from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StringConstraints


class UserServiceResponse(BaseModel):
    id: UUID
    name: str
    email: Annotated[str, StringConstraints(min_length=1)]


class CreateNotificationRequest(BaseModel):
    order_id: UUID
    email: str
    message: str
