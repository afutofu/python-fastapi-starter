from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: int = Field(gt=0)
    text: str = Field(min_length=1, max_length=100)
    completed: bool = Field(default=False)
