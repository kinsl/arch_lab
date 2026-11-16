from uuid import UUID

from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.infrastructure.repositories.users_repository import UserRepository


class GetUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID) -> User:
        return await self._repository.get(item_id)
