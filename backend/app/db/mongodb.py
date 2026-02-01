from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
# tạo biến toàn cục để giữ kết nối MongoDB
client: AsyncIOMotorClient = None
db = None

# Hàm kết nối đến MongoDB
async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]
    print("Connected to MongoDB")

# Hàm đóng kết nối MongoDB
async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")

# Hàm lấy đối tượng database
def get_database():
    return db

# Hàm lấy một collection cụ thể
def get_collection(collection_name: str):
    return db[collection_name]
