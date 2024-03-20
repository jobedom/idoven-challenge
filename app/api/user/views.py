# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, HTTPException, Path, Request

from app.lib.auth import get_current_user
from app.models import User, UserSchema

from .schema import CreateUserRequest, CreateUserResponse, ReadAllUserResponse, ReadUserResponse
from .use_cases import CreateUser, DeleteUser, ReadAllUsers, ReadUser, ReadUserByEmail

router = APIRouter(prefix="/user")


@router.post("", response_model=CreateUserResponse)
async def create(
    request: Request,
    data: CreateUserRequest,
    read_use_case: ReadUser = Depends(ReadUserByEmail),
    create_use_case: CreateUser = Depends(CreateUser),
    auth_user: User = Depends(get_current_user),
) -> UserSchema:
    if not auth_user.is_admin:
        raise HTTPException(status_code=403)
    user = await read_use_case.execute(data.email)
    if user is not None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return await create_use_case.execute(data.email, data.password, data.is_admin)


@router.get("", response_model=ReadAllUserResponse)
async def read_all(
    request: Request,
    use_case: ReadAllUsers = Depends(ReadAllUsers),
    auth_user: User = Depends(get_current_user),
) -> ReadAllUserResponse:
    if not auth_user.is_admin:
        raise HTTPException(status_code=403)
    return ReadAllUserResponse(users=[user async for user in use_case.execute()])


@router.get("/{user_id}", response_model=ReadUserResponse)
async def read(
    request: Request,
    user_id: int = Path(..., description=""),
    use_case: ReadUser = Depends(ReadUser),
    auth_user: User = Depends(get_current_user),
) -> UserSchema:
    if not auth_user.is_admin:
        raise HTTPException(status_code=403)
    user = await use_case.execute(user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete(
    request: Request,
    user_id: int = Path(..., description=""),
    use_case: DeleteUser = Depends(DeleteUser),
    auth_user: User = Depends(get_current_user),
) -> None:
    if not auth_user.is_admin:
        raise HTTPException(status_code=403)
    await use_case.execute(user_id)
