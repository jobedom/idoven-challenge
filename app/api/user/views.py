# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, HTTPException, Path, Request

from app.models import ECGSchema, User

from .schema import CreateUserRequest, CreateUserResponse, ReadAllUserResponse, ReadUserResponse
from .use_cases import CreateUser, DeleteUser, ReadAllUsers, ReadUser

router = APIRouter(prefix="/user")


@router.post("", response_model=CreateUserResponse)
async def create(
    request: Request,
    data: CreateUserRequest,
    use_case: CreateUser = Depends(CreateUser),
) -> ECGSchema:
    user = await User.get_by_email(data.email)
    if user is not None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return await use_case.execute(data.email, data.password, data.is_admin)


@router.get("", response_model=ReadAllUserResponse)
async def read_all(
    request: Request,
    use_case: ReadAllUsers = Depends(ReadAllUsers),
) -> ReadAllUserResponse:
    return ReadAllUserResponse(users=[user async for user in use_case.execute()])


@router.get("/{user_id}", response_model=ReadUserResponse)
async def read(
    request: Request,
    user_id: int = Path(..., description=""),
    use_case: ReadUser = Depends(ReadUser),
) -> ECGSchema:
    return await use_case.execute(user_id)


@router.delete("/{user_id}", status_code=204)
async def delete(
    request: Request,
    user_id: int = Path(..., description=""),
    use_case: DeleteUser = Depends(DeleteUser),
) -> None:
    await use_case.execute(user_id)
