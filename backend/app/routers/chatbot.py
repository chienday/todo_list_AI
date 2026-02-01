from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.llm_service import llm_service
from app.services.todo_service import get_todos
from app.core.security import get_current_user

router = APIRouter()


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with the AI assistant."""
    # Get user's todos for context
    user_todos = await get_todos(current_user["user_id"])
    todos_dict = [
        {
            "title": todo.title,
            "priority": todo.priority,
            "status": todo.status
        }
        for todo in user_todos
    ]
    
    # Convert messages to dict format
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    # Get response from LLM
    response = await llm_service.chat(messages, todos_dict)
    
    return ChatResponse(response=response)
