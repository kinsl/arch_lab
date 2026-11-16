from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.infrastructure.repositories.users_repository import UserRepository


class ListUsersUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, *, limit: int, offset: int) -> list[User]:
        return await self._repository.list(limit=limit, offset=offset)
