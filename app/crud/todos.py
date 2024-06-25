from typing import List
from app.models.todos import Todo, TodoInDB

# In-memory database for todos
fake_todo_db: List[TodoInDB] = [
    TodoInDB(id=1, text="Buy milk", completed=False),
    TodoInDB(id=2, text="Buy eggs", completed=True),
    TodoInDB(id=3, text="Buy bread", completed=False),
    TodoInDB(id=4, text="Buy butter", completed=True),
    TodoInDB(id=5, text="Buy sugar", completed=False),
]
next_todo_id: int = len(fake_todo_db) + 1


def get_todo_by_id(todo_id: int) -> TodoInDB | None:
    """Fetches a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item.

    Returns:
        TodoInDB | None: The todo item if found, None otherwise.
    """
    return next((todo for todo in fake_todo_db if todo.id == todo_id), None)


def get_todos() -> List[TodoInDB]:
    """Retrieves all todo items.

    Returns:
        List[TodoInDB]: The list of todo items.
    """
    return fake_todo_db


def create_todo(todo: Todo) -> TodoInDB:
    """Creates a new todo item.

    Args:
        todo (Todo): The todo item to create.

    Returns:
        TodoInDB: The created todo item.
    """
    global next_todo_id
    todo_in_db = TodoInDB(id=next_todo_id, text=todo.text, completed=todo.completed)
    fake_todo_db.append(todo_in_db)
    next_todo_id += 1
    return todo_in_db


def update_todo_by_id(todo_id: int, todo: Todo) -> TodoInDB | None:
    """Updates a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item.
        todo (Todo): The updated todo item.

    Returns:
        TodoInDB | None: The updated todo item if found, None otherwise.
    """
    index = next((i for i, t in enumerate(fake_todo_db) if t.id == todo_id), None)
    if index is None:
        return None
    updated_todo = TodoInDB(id=todo_id, text=todo.text, completed=todo.completed)
    fake_todo_db[index] = updated_todo
    return updated_todo


def delete_todo_by_id(todo_id: int) -> TodoInDB | None:
    """Deletes a todo item by its ID.

    Args:
        todo_id (int): The ID of the todo item.

    Returns:
        TodoInDB | None: The deleted todo item if found, None otherwise.
    """
    todo = next((todo for todo in fake_todo_db if todo.id == todo_id), None)
    if todo is None:
        return None
    fake_todo_db.remove(todo)
    return todo


def get_next_todo_id() -> int:
    """Gets the next available ID for a new todo item.

    Returns:
        int: The next available ID.
    """
    global next_todo_id
    return next_todo_id


def clear_todos() -> None:
    """Clears all todo items and resets the next ID."""
    global next_todo_id
    fake_todo_db.clear()
    next_todo_id = 1
    return None
