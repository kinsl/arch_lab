from uuid import UUID

from user_service.modules.users.infrastructure.repositories.users_repository import UserRepository


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID) -> None:
        await self._repository.delete(item_id)
