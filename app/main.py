from fastapi import FastAPI
from .routers import todos

app = FastAPI()


app.include_router(todos.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
