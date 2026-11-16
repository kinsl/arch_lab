from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, Response

from user_service.modules.users.application.use_cases.create_user_use_case import CreateUserUseCase
from user_service.modules.users.application.use_cases.delete_user_use_case import DeleteUserUseCase
from user_service.modules.users.application.use_cases.get_user_use_case import GetUserUseCase
from user_service.modules.users.application.use_cases.list_users_use_case import ListUsersUseCase
from user_service.modules.users.application.use_cases.update_user_use_case import UpdateUserUseCase
from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.presentation.http.schemas import CreateUserBody, UpdateUserBody, UserResponse

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post("", response_model=UserResponse, status_code=201)
async def create(body: CreateUserBody, use_case: FromDishka[CreateUserUseCase]) -> User:
    return await use_case.execute(body.to_dto())


@router.get("", response_model=list[UserResponse])
async def list_items(
    use_case: FromDishka[ListUsersUseCase],
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[User]:
    return await use_case.execute(limit=limit, offset=offset)


@router.get("/{item_id}", response_model=UserResponse)
async def get(item_id: UUID, use_case: FromDishka[GetUserUseCase]) -> User:
    return await use_case.execute(item_id)


@router.put("/{item_id}", response_model=UserResponse)
async def update(item_id: UUID, body: UpdateUserBody, use_case: FromDishka[UpdateUserUseCase]) -> User:
    return await use_case.execute(item_id, body.to_dto())


@router.delete("/{item_id}", status_code=204)
async def delete(item_id: UUID, use_case: FromDishka[DeleteUserUseCase]) -> Response:
    await use_case.execute(item_id)
    return Response(status_code=204)
