from typing import List
from fastapi import APIRouter, HTTPException

from ..models.todos import Todo

router = APIRouter(
    prefix="/todos",
    # tags=["items"],
    # responses={404: {"description": "Not found"}},
)

todosMock: List[Todo] = [
    Todo(id=1, text="Buy milk", completed=False),
    Todo(id=2, text="Buy eggs", completed=True),
    Todo(id=3, text="Buy bread", completed=False),
    Todo(id=4, text="Buy butter", completed=True),
    Todo(id=5, text="Buy sugar", completed=False),
]


@router.get("/")
async def get_todos() -> List[Todo]:
    return todosMock


@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: int) -> Todo | dict[str, str]:
    for todo in todosMock:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("")
async def create_todo(todo: Todo) -> Todo:
    todosMock.append(todo)
    return todo


@router.put("/{todo_id}")
async def update_todo_by_id(todo_id: int, todo: Todo) -> Todo | dict[str, str]:
    for index, t in enumerate(todosMock):
        if t.id == todo_id:
            todosMock[index] = todo
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}")
async def delete_todo_by_id(todo_id: int) -> dict[str, str]:
    for index, t in enumerate(todosMock):
        if t.id == todo_id:
            del todosMock[index]
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
