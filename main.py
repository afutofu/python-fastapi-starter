from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: int = Field(gt=0)
    text: str = Field(min_length=1, max_length=100)
    completed: bool = Field(default=False)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


todosMock: List[Todo] = [
    Todo(id=1, text="Buy milk", completed=False),
    Todo(id=2, text="Buy eggs", completed=True),
    Todo(id=3, text="Buy bread", completed=False),
    Todo(id=4, text="Buy butter", completed=True),
    Todo(id=5, text="Buy sugar", completed=False),
]


@app.get("/todos")
async def get_todos() -> List[Todo]:
    return todosMock


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int) -> Todo | dict[str, str]:
    for todo in todosMock:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos")
async def create_todo(todo: Todo) -> Todo:
    todosMock.append(todo)
    return todo


@app.put("/todos/{todo_id}")
async def update_todo_by_id(todo_id: int, todo: Todo) -> Todo | dict[str, str]:
    for index, t in enumerate(todosMock):
        if t.id == todo_id:
            todosMock[index] = todo
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo_by_id(todo_id: int) -> dict[str, str]:
    for index, t in enumerate(todosMock):
        if t.id == todo_id:
            del todosMock[index]
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
