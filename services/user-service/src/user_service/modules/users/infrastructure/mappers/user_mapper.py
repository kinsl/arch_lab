from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.infrastructure.rows import UserRow


class UserMapper:
    @staticmethod
    def to_entity(row: UserRow) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
        )
