from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..models.todos import Todo, TodoInDB
from ..crud import todos as todos_crud

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[TodoInDB])
async def get_todos() -> List[TodoInDB]:
    """Retrieves all todo items.

    Returns:
        List[TodoInDB]: The list of todo items.
    """

    return todos_crud.get_todos()


@router.get(
    "/{todo_id}",
    response_model=TodoInDB,
    responses={404: {"description": "Todo not found"}},
)
async def get_todo_by_id(
    todo_id: int,
) -> TodoInDB | dict[str, str]:
    """Fetches a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item.

    Returns:
        TodoInDB | dict[str, str]: The todo item if found, error otherwise.
    """

    todo = todos_crud.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post(
    "",
    response_model=TodoInDB,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Todo successfully created"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
    },
)
async def create_todo(
    todo: Todo,
) -> TodoInDB:
    """Creates a new todo item.

    Args:
        todo (Todo): The todo item to create.

    Returns:
        TodoInDB: The created todo item.
    """

    return todos_crud.create_todo(todo)


@router.put(
    "/{todo_id}",
    response_model=TodoInDB,
    responses={404: {"description": "Todo not found"}},
)
async def update_todo_by_id(
    todo_id: int,
    todo: Todo,
) -> TodoInDB | dict[str, str]:
    """Updates a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item.
        todo (Todo): The updated todo item.

    Returns:
        TodoInDB | dict[str, str]: The updated todo item if found, or an error message if not found.
    """

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
    todo_id: int,
) -> dict[str, str]:
    """Deletes a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item.

    Returns:
        dict[str, str]: A message indicating whether the deletion was successful or an error message if not found.
    """

    deleted_todo = todos_crud.delete_todo_by_id(todo_id)
    if deleted_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return {"message": "Todo deleted"}
