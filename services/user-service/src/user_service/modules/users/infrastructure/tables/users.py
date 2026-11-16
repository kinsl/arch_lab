from uuid import uuid4

from sqlalchemy import Column, String, Table, Uuid

from user_service.core.db.database import metadata

users_table = Table(
    "users",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(320), nullable=False),
    Column("email", String(320), nullable=False, unique=True),
)
