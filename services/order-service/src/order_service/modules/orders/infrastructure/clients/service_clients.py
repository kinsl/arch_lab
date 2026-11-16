import asyncio
import logging
from uuid import UUID

from httpx2 import AsyncClient, HTTPError, Response
from pydantic import ValidationError

from order_service.modules.orders.domain.errors import DependencyUnavailableError, InvalidUserError
from order_service.modules.orders.infrastructure.clients.schemas import CreateNotificationRequest, UserServiceResponse

logger = logging.getLogger(__name__)


class HttpUserGateway:
    def __init__(self, client: AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")

    async def get_email(self, user_id: UUID) -> str:
        response = await self._get_user(user_id)
        try:
            user = UserServiceResponse.model_validate_json(response.content)
        except ValidationError as exc:
            raise DependencyUnavailableError("Invalid User Service response") from exc
        return user.email

    async def _get_user(self, user_id: UUID) -> Response:
        for attempt in range(3):
            try:
                response = await self._client.get(f"{self._base_url}/users/{user_id}")
            except HTTPError as exc:
                if attempt == 2:
                    raise DependencyUnavailableError("User Service temporarily unavailable") from exc
            else:
                if response.status_code == 404:
                    raise InvalidUserError("User does not exist")
                if response.is_success:
                    return response
                if attempt == 2:
                    raise DependencyUnavailableError("User Service temporarily unavailable")
            await asyncio.sleep(0.1 * (2**attempt))
        raise DependencyUnavailableError("User Service temporarily unavailable")


class HttpNotificationGateway:
    def __init__(self, client: AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")

    async def send(self, order_id: UUID, email: str) -> None:
        try:
            response = await self._client.post(
                f"{self._base_url}/notifications",
                json=CreateNotificationRequest(
                    order_id=order_id,
                    email=email,
                    message=f"Заказ {order_id} создан",
                ).model_dump(mode="json"),
            )
            response.raise_for_status()
        except HTTPError as exc:
            logger.warning("Notification Service request failed: %s", type(exc).__name__)
            raise DependencyUnavailableError("Notification Service temporarily unavailable") from exc
