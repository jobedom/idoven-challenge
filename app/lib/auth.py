# pylint: disable=raise-missing-from

import ast
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.api.login.schema import TokenPayloadSchema, TokenSchema
from app.api.user.schema import UserSchema
from app.api.user.use_cases import ReadUserByEmail
from app.settings import settings

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def get_current_user(
    token: str = Depends(reuseable_oauth), use_case: ReadUserByEmail = Depends(ReadUserByEmail)
) -> UserSchema:
    try:
        payload: TokenSchema = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])

        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_subject = TokenPayloadSchema(**ast.literal_eval((payload["sub"])))
    user = await use_case.execute(email=auth_subject.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user
