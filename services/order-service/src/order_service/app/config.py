import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    database_url: str
    user_service_url: str = "http://user-service:8000"
    notification_service_url: str = "http://notification-service:8000"

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            database_url=os.environ["DATABASE_URL"],
            user_service_url=os.getenv("USER_SERVICE_URL", "http://user-service:8000"),
            notification_service_url=os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8000"),
        )
