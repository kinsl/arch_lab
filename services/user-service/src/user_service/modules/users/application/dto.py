from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    name: str
    email: str


@dataclass(frozen=True, slots=True)
class UpdateUserDTO:
    name: str
    email: str
