from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.schemas import Todo, TodoCreate, TodoStats, TodoUpdate
from app.store import TodoStore

router = APIRouter()


def get_store(request: Request) -> TodoStore:
    return request.app.state.todo_store


Store = Annotated[TodoStore, Depends(get_store)]


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/stats", response_model=TodoStats, tags=["todos"])
def stats(store: Store) -> TodoStats:
    return store.stats()


@router.get("/api/todos", response_model=list[Todo], tags=["todos"])
def list_todos(store: Store) -> list[Todo]:
    return store.list()


@router.post(
    "/api/todos",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,
    tags=["todos"],
)
def create_todo(data: TodoCreate, store: Store) -> Todo:
    return store.create(data)


@router.get("/api/todos/{todo_id}", response_model=Todo, tags=["todos"])
def get_todo(todo_id: int, store: Store) -> Todo:
    todo = store.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/api/todos/{todo_id}", response_model=Todo, tags=["todos"])
def update_todo(todo_id: int, data: TodoUpdate, store: Store) -> Todo:
    todo = store.update(todo_id, data)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete(
    "/api/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["todos"],
)
def delete_todo(todo_id: int, store: Store) -> Response:
    if not store.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
