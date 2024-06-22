from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models.todos import Todo

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

todos_mock: List[Todo] = [
    Todo(id=1, text="Buy milk", completed=False),
    Todo(id=2, text="Buy eggs", completed=True),
    Todo(id=3, text="Buy bread", completed=False),
    Todo(id=4, text="Buy butter", completed=True),
    Todo(id=5, text="Buy sugar", completed=False),
]


@router.get("", response_model=List[Todo])
async def get_todos() -> List[Todo]:
    return todos_mock


@router.get(
    "/{todo_id}",
    response_model=Todo,
    responses={404: {"description": "Todo not found"}},
)
async def get_todo_by_id(todo_id: int) -> Todo | dict[str, str]:
    todo = next((todo for todo in todos_mock if todo.id == todo_id), None)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo) -> Todo:
    todos_mock.append(todo)
    return todo


@router.put(
    "/{todo_id}",
    response_model=Todo,
    responses={404: {"description": "Todo not found"}},
)
async def update_todo_by_id(todo_id: int, todo: Todo) -> Todo | dict[str, str]:
    index = next((i for i, t in enumerate(todos_mock) if t.id == todo_id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todos_mock[index] = todo
    return todo


@router.delete(
    "/{todo_id}",
    responses={
        404: {"description": "Todo not found"},
        200: {"description": "Todo deleted"},
    },
)
async def delete_todo_by_id(todo_id: int) -> dict[str, str]:
    index = next((i for i, t in enumerate(todos_mock) if t.id == todo_id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    del todos_mock[index]
    return {"message": "Todo deleted"}
