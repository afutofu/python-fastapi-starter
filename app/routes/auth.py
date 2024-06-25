from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from pydantic import BaseModel

from ..models.users import User, UserCreate, UserInDB
from ..utils import (
    authenticate_user,
    blacklist_token,
    create_access_token,
    fake_users_db,
    next_user_id,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=User)
async def register_user(user: UserCreate):
    """Registers a new user.

    Args:
        user (UserCreate): The user details for registration.

    Raises:
        HTTPException: If the username is already registered.

    Returns:
        User: The registered user.
    """

    for user_in_db in fake_users_db:
        if user.username == user_in_db.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
    hashed_password = get_password_hash(user.password)
    global next_user_id
    user_in_db = UserInDB(
        id=next_user_id,
        username=user.username,
        hashed_password=hashed_password,
    )
    fake_users_db.append(user_in_db)
    next_user_id += 1
    return user_in_db


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Logs in a user and returns an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        Token: The access token and token type.
    """

    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """Logs out a user by blacklisting the access token.

    Args:
        token (str): The JWT token of the user.

    Returns:
        dict: A message indicating that the logout was successful.
    """

    blacklist_token(token)
    return {"message": "Logout successful"}
