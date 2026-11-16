from uuid import UUID

from user_service.modules.users.application.dto import UpdateUserDTO
from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.infrastructure.repositories.users_repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID, data: UpdateUserDTO) -> User:
        return await self._repository.update(item_id, data)
