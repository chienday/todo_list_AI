from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str = "mongodb://mongo:27017"
    database_name: str = "todo_ai_db"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LLM
    llm_api_key: str = ""
    llm_model: str = "gpt-3.5-turbo"
    # basesetting đọc env
    class Config:
        env_file = ".env"

# sigleton pattern để lấy settings
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
