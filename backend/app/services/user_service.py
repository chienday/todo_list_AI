from typing import Optional
from datetime import datetime
from bson import ObjectId

from app.db.mongodb import get_collection
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password


USERS_COLLECTION = "users"


async def create_user(user_data: UserCreate) -> UserResponse:
    users = get_collection(USERS_COLLECTION)
    
    # Check if user exists
    existing_user = await users.find_one({"email": user_data.email})
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Create user
    user_dict = {
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": get_password_hash(user_data.password),
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    
    result = await users.insert_one(user_dict)
    created_user = await users.find_one({"_id": result.inserted_id})
    
    return UserResponse(
        id=str(created_user["_id"]),
        email=created_user["email"],
        username=created_user["username"],
        created_at=created_user.get("created_at"),
        is_active=created_user.get("is_active", True)
    )


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    users = get_collection(USERS_COLLECTION)
    user = await users.find_one({"email": email})
    
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user


async def get_user_by_id(user_id: str) -> Optional[dict]:
    users = get_collection(USERS_COLLECTION)
    user = await users.find_one({"_id": ObjectId(user_id)})
    return user
