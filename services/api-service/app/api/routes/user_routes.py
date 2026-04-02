from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUserDep, UserServiceDep
from app.schemas.user import UserReadWithoutPassword
from app.core.settings import settings
from app.core.security import create_token, validate_token, verify_password
from app.schemas.base import Message
from app.schemas.user import Token, UpdatePassword, UserCreate, UserRegister

router = APIRouter(tags=["Login"])


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    response: Response,
    user_service: UserServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not await user_service.authenticate_user(
        form_data.username, form_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    acces_token_data = {
        "type": "access",
        "sub": str(user.id),
    }
    access_token = create_token(
        subject=acces_token_data, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_data = {
        "type": "refresh",
        "sub": str(user.id),
    }
    refresh_token = create_token(
        subject=refresh_token_data, expires_delta=refresh_token_expires
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return Token(access_token=access_token, user_id=user.id)


@router.post("/signup", response_model=Message, status_code=status.HTTP_201_CREATED)
async def register_user(user_service: UserServiceDep, user_in: UserRegister):
    user = await user_service.get_user_by_username(user_in.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    user_create = UserCreate(username=user_in.username, password=user_in.password)
    await user_service.create_user(user_create)
    return Message(message="User successfully signed up")


@router.get("/me", response_model=UserReadWithoutPassword)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.patch("/change-password", response_model=Message)
async def change_password(
    user_service: UserServiceDep, current_user: CurrentUserDep, body: UpdatePassword
):
    verified, _ = verify_password(body.current_password, current_user.hashed_password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current password",
        )
    await user_service.update_user_password(current_user.id, body.new_password)
    return Message(message="Password successfully changed")


@router.post("/logout")
async def logout(response: Response, current_user: CurrentUserDep):
    response.delete_cookie("refresh_token")
    return Message(message="You have been logged out")


@router.post("/refresh", response_model=Token)
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing",
        )
    payload = validate_token(refresh_token, "refresh")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "type": "access",
        "sub": payload.get("sub"),
    }
    access_token = create_token(
        subject=access_token_data, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_data = {
        "type": "refresh",
        "sub": payload.get("sub"),
    }
    refresh_token = create_token(
        subject=refresh_token_data, expires_delta=refresh_token_expires
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return Token(access_token=access_token, user_id=payload.get("sub"))
