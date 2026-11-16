from uuid import uuid4

from sqlalchemy import Column, Integer, String, Table, Uuid

from order_service.core.db.database import metadata

orders_table = Table(
    "orders",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", Uuid(as_uuid=True), nullable=False),
    Column("product", String(320), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("email", String(320), nullable=False),
    Column("notification_status", String(320), nullable=False),
)
