from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

from user_service.modules.users.application.dto import CreateUserDTO, UpdateUserDTO

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)]


class CreateUserBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Text
    email: EmailStr

    def to_dto(self) -> CreateUserDTO:
        return CreateUserDTO(name=self.name, email=str(self.email))


class UpdateUserBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Text
    email: EmailStr

    def to_dto(self) -> UpdateUserDTO:
        return UpdateUserDTO(name=self.name, email=str(self.email))


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    email: str
