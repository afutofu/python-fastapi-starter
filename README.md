# Python FastAPI Starter

This branch includes a starter implementation of a todo API in Python FastAPI.

Access other branches to find more modular implementations of authentication and todo APIs:

- [main](https://github.com/afutofu/python-fastapi-starter): Auth & Todo API
- [rest-auth](https://github.com/afutofu/python-fastapi-starter/tree/rest-auth): Auth API

## Table of Contents

1. [Features](#features)
1. [Endpoints](#endpoints)
1. [Setup](#setup)
1. [Usage](#usage)
1. [Access OpenAPI](#access-openapi-ui)
1. [Authors](#authors)

## Features

- Create a todo
- Get all todos
- Get a todo by ID
- Update a todo by ID
- Delete a todo by ID

## Endpoints

### Todo

- `POST /todos` - Create a new todo
- `GET /todos` - Get all todos
- `GET /todos/{id}` - Get a todo by ID
- `PUT /todos/{id}` - Update a todo by ID
- `DELETE /todos/{id}` - Delete a todo by ID
  I

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/afutofu/python-fastapi-starter.git
   cd python-fastapi-starter
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:

   ```bash
    uvicorn folder.main:app --reload
   ```

## Usage

### Todo

Create a Todo:

```bash
curl -X POST http://localhost:8000/todos -H "Content-Type: application/json" -d '{"text":"Test Todo", "completed":false}'
```

Get All Todos:

```bash
curl -X GET http://localhost:8000/todos
```

Get a Todo by ID:

```bash
curl -X GET http://localhost:8000/todos/1
```

Update a Todo by ID:

```bash
curl -X PUT http://localhost:8000/todos/1 -H "Content-Type: application/json" -d '{"text":"Updated Todo", "completed":true}'
```

Delete a Todo by ID:

```bash
curl -X DELETE http://localhost:8000/todos/1
```

## Access OpenAPI UI

Navigate to:

```bash
http://localhost:8000/docs
```

![OpenAPI (Swagger) UI](openapi-image.png)

## Authors

- [Afuza](https://github.com/afutofu): Create and maintain repository
