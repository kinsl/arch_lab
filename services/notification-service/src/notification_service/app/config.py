import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    database_url: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            database_url=os.environ["DATABASE_URL"],
        )
