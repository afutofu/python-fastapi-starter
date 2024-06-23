from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserCreate(User):
    password: str


class UserInDB(User):
    id: int
    hashed_password: str
