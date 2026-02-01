from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services.todo_service import (
    create_todo,
    get_todos,
    get_todo_by_id,
    update_todo,
    delete_todo
)
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    todo_data: TodoCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new todo."""
    todo = await create_todo(current_user["user_id"], todo_data)
    return todo


@router.get("/", response_model=List[TodoResponse])
async def list_todos(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all todos for the current user."""
    todos = await get_todos(current_user["user_id"], skip, limit)
    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific todo by ID."""
    todo = await get_todo_by_id(todo_id, current_user["user_id"])
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_existing_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a todo."""
    todo = await update_todo(todo_id, current_user["user_id"], todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_todo(
    todo_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a todo."""
    deleted = await delete_todo(todo_id, current_user["user_id"])
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
