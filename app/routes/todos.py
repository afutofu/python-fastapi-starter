from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.dependencies import get_current_user
from app.models.users import UserInDB

from ..models.todos import Todo, TodoInDB
from ..utils import fake_todo_db, next_todo_id

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[TodoInDB])
async def get_todos(
    current_user: UserInDB = Depends(get_current_user),
) -> List[TodoInDB]:
    return fake_todo_db


@router.get(
    "/{todo_id}",
    response_model=TodoInDB,
    responses={404: {"description": "Todo not found"}},
)
async def get_todo_by_id(
    todo_id: int, current_user: UserInDB = Depends(get_current_user)
) -> TodoInDB | dict[str, str]:
    todo = next((todo for todo in fake_todo_db if todo.id == todo_id), None)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: Todo, current_user: UserInDB = Depends(get_current_user)
) -> TodoInDB:
    global next_todo_id
    print(next_todo_id, todo.text, todo.completed)
    todo_in_db = TodoInDB(id=next_todo_id, text=todo.text, completed=todo.completed)
    fake_todo_db.append(todo_in_db)
    next_todo_id += 1
    return todo_in_db


@router.put(
    "/{todo_id}",
    response_model=TodoInDB,
    responses={404: {"description": "Todo not found"}},
)
async def update_todo_by_id(
    todo_id: int, todo: Todo, current_user: UserInDB = Depends(get_current_user)
) -> TodoInDB | dict[str, str]:
    index = next((i for i, t in enumerate(fake_todo_db) if t.id == todo_id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo_in_db = TodoInDB(id=todo_id, **todo.model_dump())
    fake_todo_db[index] = todo_in_db
    return todo_in_db


@router.delete(
    "/{todo_id}",
    responses={
        404: {"description": "Todo not found"},
        200: {"description": "Todo deleted"},
    },
)
async def delete_todo_by_id(
    todo_id: int, current_user: UserInDB = Depends(get_current_user)
) -> dict[str, str]:
    index = next((i for i, t in enumerate(fake_todo_db) if t.id == todo_id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    del fake_todo_db[index]
    return {"message": "Todo deleted"}
