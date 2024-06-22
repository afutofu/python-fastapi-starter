from typing import List
from fastapi import FastAPI
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    text: str
    completed: bool


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
    return {"message": "Todo not found"}


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
    return {"message": "Todo not found"}


@app.delete("/todos/{todo_id}")
async def delete_todo_by_id(todo_id: int) -> dict[str, str]:
    for index, t in enumerate(todosMock):
        if t.id == todo_id:
            del todosMock[index]
            return {"message": "Todo deleted"}
    return {"message": "Todo not found"}
