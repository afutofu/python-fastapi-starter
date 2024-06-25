from fastapi import FastAPI
from .routes import todos

app = FastAPI()

app.include_router(todos.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
