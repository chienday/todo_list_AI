from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.todo import Priority, Status


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None


class TodoResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    priority: Priority
    status: Status
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoResponse]
    total: int
