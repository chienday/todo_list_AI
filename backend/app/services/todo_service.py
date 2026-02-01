from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.db.mongodb import get_collection
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse


TODOS_COLLECTION = "todos"


async def create_todo(user_id: str, todo_data: TodoCreate) -> TodoResponse:
    todos = get_collection(TODOS_COLLECTION)
    
    todo_dict = {
        "user_id": user_id,
        "title": todo_data.title,
        "description": todo_data.description,
        "priority": todo_data.priority.value,
        "status": "pending",
        "due_date": todo_data.due_date,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    result = await todos.insert_one(todo_dict)
    created_todo = await todos.find_one({"_id": result.inserted_id})
    
    return _todo_to_response(created_todo)


async def get_todos(user_id: str, skip: int = 0, limit: int = 100) -> List[TodoResponse]:
    todos = get_collection(TODOS_COLLECTION)
    cursor = todos.find({"user_id": user_id}).skip(skip).limit(limit)
    
    result = []
    async for todo in cursor:
        result.append(_todo_to_response(todo))
    
    return result


async def get_todo_by_id(todo_id: str, user_id: str) -> Optional[TodoResponse]:
    todos = get_collection(TODOS_COLLECTION)
    todo = await todos.find_one({"_id": ObjectId(todo_id), "user_id": user_id})
    
    if todo:
        return _todo_to_response(todo)
    return None


async def update_todo(todo_id: str, user_id: str, todo_data: TodoUpdate) -> Optional[TodoResponse]:
    todos = get_collection(TODOS_COLLECTION)
    
    update_dict = {"updated_at": datetime.utcnow()}
    
    if todo_data.title is not None:
        update_dict["title"] = todo_data.title
    if todo_data.description is not None:
        update_dict["description"] = todo_data.description
    if todo_data.priority is not None:
        update_dict["priority"] = todo_data.priority.value
    if todo_data.status is not None:
        update_dict["status"] = todo_data.status.value
    if todo_data.due_date is not None:
        update_dict["due_date"] = todo_data.due_date
    
    result = await todos.find_one_and_update(
        {"_id": ObjectId(todo_id), "user_id": user_id},
        {"$set": update_dict},
        return_document=True
    )
    
    if result:
        return _todo_to_response(result)
    return None


async def delete_todo(todo_id: str, user_id: str) -> bool:
    todos = get_collection(TODOS_COLLECTION)
    result = await todos.delete_one({"_id": ObjectId(todo_id), "user_id": user_id})
    return result.deleted_count > 0


def _todo_to_response(todo: dict) -> TodoResponse:
    return TodoResponse(
        id=str(todo["_id"]),
        user_id=todo["user_id"],
        title=todo["title"],
        description=todo.get("description"),
        priority=todo["priority"],
        status=todo["status"],
        due_date=todo.get("due_date"),
        created_at=todo["created_at"],
        updated_at=todo["updated_at"],
    )
