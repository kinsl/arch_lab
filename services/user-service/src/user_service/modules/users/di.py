from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection

from user_service.modules.users.application.use_cases.create_user_use_case import CreateUserUseCase
from user_service.modules.users.application.use_cases.delete_user_use_case import DeleteUserUseCase
from user_service.modules.users.application.use_cases.get_user_use_case import GetUserUseCase
from user_service.modules.users.application.use_cases.list_users_use_case import ListUsersUseCase
from user_service.modules.users.application.use_cases.update_user_use_case import UpdateUserUseCase
from user_service.modules.users.infrastructure.repositories.users_repository import UserRepository


class UserProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def repository(self, connection: AsyncConnection) -> UserRepository:
        return UserRepository(connection)

    @provide
    def create_user(self, repository: UserRepository) -> CreateUserUseCase:
        return CreateUserUseCase(repository)

    @provide
    def get_user(self, repository: UserRepository) -> GetUserUseCase:
        return GetUserUseCase(repository)

    @provide
    def list_users(self, repository: UserRepository) -> ListUsersUseCase:
        return ListUsersUseCase(repository)

    @provide
    def update_user(self, repository: UserRepository) -> UpdateUserUseCase:
        return UpdateUserUseCase(repository)

    @provide
    def delete_user(self, repository: UserRepository) -> DeleteUserUseCase:
        return DeleteUserUseCase(repository)
