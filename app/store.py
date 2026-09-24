from datetime import UTC, datetime
from threading import Lock

from app.schemas import Todo, TodoCreate, TodoStats, TodoUpdate


class TodoStore:
    """Small thread-safe in-memory repository for todo records."""

    def __init__(self) -> None:
        self._items: dict[int, Todo] = {}
        self._next_id = 1
        self._lock = Lock()

    def list(self) -> list[Todo]:
        with self._lock:
            return list(self._items.values())

    def get(self, todo_id: int) -> Todo | None:
        with self._lock:
            return self._items.get(todo_id)

    def create(self, data: TodoCreate) -> Todo:
        with self._lock:
            todo = Todo(
                id=self._next_id,
                title=data.title,
                completed=False,
                created_at=datetime.now(UTC),
                completed_at=None,
            )
            self._items[todo.id] = todo
            self._next_id += 1
            return todo

    def update(self, todo_id: int, data: TodoUpdate) -> Todo | None:
        with self._lock:
            current = self._items.get(todo_id)
            if current is None:
                return None
            changes = data.model_dump(exclude_none=True)
            if data.completed is not None and data.completed != current.completed:
                changes["completed_at"] = datetime.now(UTC) if data.completed else None
            updated = current.model_copy(update=changes) if changes else current
            self._items[todo_id] = updated
            return updated

    def delete(self, todo_id: int) -> bool:
        with self._lock:
            return self._items.pop(todo_id, None) is not None

    def stats(self) -> TodoStats:
        with self._lock:
            completed = sum(item.completed for item in self._items.values())
            total = len(self._items)
            return TodoStats(total=total, completed=completed, pending=total - completed)
