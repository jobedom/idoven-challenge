# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.user.use_cases import ReadUserByEmail
from app.lib.password import verify_password
from app.lib.token import create_access_token, create_refresh_token

from .schema import LoginResponseSchema

router = APIRouter(prefix="")


@router.post("/login", response_model=LoginResponseSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), use_case: ReadUserByEmail = Depends(ReadUserByEmail)):
    user = await use_case.execute(form_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    subject = {"id": user.id, "email": user.email, "is_admin": user.is_admin}

    return {
        "access_token": create_access_token(subject),
        "refresh_token": create_refresh_token(subject),
    }
