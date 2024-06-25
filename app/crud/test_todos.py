from ..models.todos import Todo, TodoInDB
from .todos import (
    fake_todo_db,
    get_todo_by_id,
    get_todos,
    create_todo,
    update_todo_by_id,
    delete_todo_by_id,
    get_next_todo_id,
    clear_todos,
)


def create_mock_todos():
    for i in range(1, 6):
        create_todo(Todo(text=f"Buy item {i}", completed=False))


def test_get_todo_by_id():
    clear_todos()

    # Create some todos
    create_mock_todos()

    todo = get_todo_by_id(1)
    assert todo is not None
    assert todo.id == 1
    assert todo.text == "Buy item 1"

    todo = get_todo_by_id(999)
    assert todo is None


def test_get_todos():
    clear_todos()

    # Create some todos
    create_mock_todos()

    todos = get_todos()
    assert len(todos) == 5
    assert todos[0].text == "Buy item 1"


def test_create_todo():
    clear_todos()

    # Create some todos
    create_mock_todos()

    new_todo = Todo(text="Test todo", completed=False)
    created_todo = create_todo(new_todo)
    assert created_todo.id == 6
    assert created_todo.text == "Test todo"
    assert len(fake_todo_db) == 6


def test_update_todo_by_id():
    clear_todos()

    # Create some todos
    create_mock_todos()

    updated_todo = Todo(text="Updated todo", completed=True)
    result = update_todo_by_id(1, updated_todo)
    assert result is not None
    assert result.text == "Updated todo"
    assert fake_todo_db[0].text == "Updated todo"

    result = update_todo_by_id(999, updated_todo)
    assert result is None


def test_delete_todo_by_id():
    clear_todos()

    # Create some todos
    create_mock_todos()

    result = delete_todo_by_id(1)
    assert result is not None
    assert result.id == 1
    assert len(fake_todo_db) == 4

    result = delete_todo_by_id(999)
    assert result is None
    assert len(fake_todo_db) == 4


def test_get_next_todo_id():
    clear_todos()

    # Create some todos
    create_mock_todos()

    next_id = get_next_todo_id()
    assert next_id == 6


def test_clear_todos():
    clear_todos()

    # Create some todos
    create_mock_todos()

    clear_todos()
    assert len(fake_todo_db) == 0
    assert get_next_todo_id() == 1
