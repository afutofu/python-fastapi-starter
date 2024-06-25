from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.dependencies import get_current_user
from app.models.users import UserInDB

from ..models.todos import Todo, TodoInDB
from ..crud import todos as todos_crud

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[TodoInDB])
async def get_todos(
    current_user: UserInDB = Depends(get_current_user),
) -> List[TodoInDB]:
    return todos_crud.get_todos()


@router.get(
    "/{todo_id}",
    response_model=TodoInDB,
    responses={404: {"description": "Todo not found"}},
)
async def get_todo_by_id(
    todo_id: int, current_user: UserInDB = Depends(get_current_user)
) -> TodoInDB | dict[str, str]:
    todo = todos_crud.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: Todo, current_user: UserInDB = Depends(get_current_user)
) -> TodoInDB:
    return todos_crud.create_todo(todo)


@router.put(
    "/{todo_id}",
    response_model=TodoInDB,
    responses={404: {"description": "Todo not found"}},
)
async def update_todo_by_id(
    todo_id: int, todo: Todo, current_user: UserInDB = Depends(get_current_user)
) -> TodoInDB | dict[str, str]:
    updated_todo = todos_crud.update_todo_by_id(todo_id, todo)
    if updated_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return updated_todo


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
    deleted_todo = todos_crud.delete_todo_by_id(todo_id)
    if deleted_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return {"message": "Todo deleted"}
