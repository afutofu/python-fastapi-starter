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


# todosMock: Todo = [{}]


@app.get("/todos")
async def get_todos():
    return {"message": "Get todos"}


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    return {"message": "Get todos by id", "id": todo_id}


@app.post("/todos")
async def create_todo(todo: Todo):

    return todo
