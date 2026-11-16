from user_service.modules.users.application.dto import CreateUserDTO
from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.infrastructure.repositories.users_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, data: CreateUserDTO) -> User:
        return await self._repository.add(data)
