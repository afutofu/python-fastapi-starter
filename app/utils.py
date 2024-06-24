import jwt
from datetime import datetime, timedelta
from typing import List, Optional

from app.models.todos import TodoInDB
from .models.users import User, UserInDB
from passlib.context import CryptContext

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


fake_todo_db: List[TodoInDB] = [
    TodoInDB(id=1, text="Buy milk", completed=False),
    TodoInDB(id=2, text="Buy eggs", completed=True),
    TodoInDB(id=3, text="Buy bread", completed=False),
    TodoInDB(id=4, text="Buy butter", completed=True),
    TodoInDB(id=5, text="Buy sugar", completed=False),
]
next_todo_id: int = len(fake_todo_db) + 1


fake_users_db: List[UserInDB] = [
    UserInDB(
        id=1, username="string", hashed_password=get_password_hash("string")
    )  # password: string
]
next_user_id: int = len(fake_users_db) + 1

token_blacklist = set()  # Store blacklisted token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: List[User], username: str) -> UserInDB | None:
    for user in db:
        if user.username == username:
            return UserInDB(**user.model_dump())
    return None


def authenticate_user(fake_db, username: str, password: str) -> UserInDB | None:
    user = get_user(fake_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return UserInDB(**user.model_dump())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def is_token_blacklisted(token: str) -> bool:
    return token in token_blacklist


def blacklist_token(token: str):
    token_blacklist.add(token)
