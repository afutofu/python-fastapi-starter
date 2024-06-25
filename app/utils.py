import jwt
from datetime import datetime, timedelta
from typing import List, Optional

from .models.users import User, UserInDB
from passlib.context import CryptContext

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """Hashes a plain text password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """

    return pwd_context.hash(password)


fake_users_db: List[UserInDB] = [
    UserInDB(
        id=1, username="string", hashed_password=get_password_hash("string")
    )  # password: string
]
next_user_id: int = len(fake_users_db) + 1

token_blacklist = set()  # Store blacklisted token


def verify_password(plain_password, hashed_password):
    """Verifies a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: List[User], username: str) -> UserInDB | None:
    """Gets a user by username.

    Args:
        db (List[User]): The list of users.
        username (str): The username.

    Returns:
        UserInDB | None: The user if found, None otherwise.
    """

    for user in db:
        if user.username == username:
            return UserInDB(**user.model_dump())
    return None


def authenticate_user(fake_db, username: str, password: str) -> UserInDB | None:
    """Authenticates a user by username and password.

    Args:
        fake_db (dict): The fake database of users.
        username (str): The username.
        password (str): The plain text password.

    Returns:
        TodoInDB | None: The authenticated user or None if authentication fails.
    """

    user = get_user(fake_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return UserInDB(**user.model_dump())


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta], optional): The token expiry time. Defaults to 15 minutes if None.

    Returns:
        str: The encoded JWT token.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def is_token_blacklisted(token: str) -> bool:
    """Checks if a token is blacklisted.

    Args:
        token (str): The JWT token.

    Returns:
        bool: True if the token is blacklisted, False otherwise.
    """

    return token in token_blacklist


def blacklist_token(token: str):
    """Adds a token to the blacklist.

    Args:
        token (str): The JWT token to blacklist.
    """

    token_blacklist.add(token)
