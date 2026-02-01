from typing import List, Dict
import httpx

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.base_url = "https://api.openai.com/v1"
    
    async def chat(self, messages: List[Dict[str, str]], user_todos: List[dict] = None) -> str:
        """
        Send a chat message to the LLM and get a response.
        Optionally include user's todos for context.
        """
        system_message = self._build_system_message(user_todos)
        
        full_messages = [
            {"role": "system", "content": system_message},
            *messages
        ]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": full_messages,
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _build_system_message(self, user_todos: List[dict] = None) -> str:
        base_message = """You are a helpful AI assistant for a Todo application. 
You help users manage their tasks, provide productivity tips, and answer questions about their todos.
Be concise, friendly, and helpful."""
        
        if user_todos:
            todos_context = "\n\nUser's current todos:\n"
            for todo in user_todos:
                todos_context += f"- {todo['title']} (Priority: {todo['priority']}, Status: {todo['status']})\n"
            return base_message + todos_context
        
        return base_message


llm_service = LLMService()
