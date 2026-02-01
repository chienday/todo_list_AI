from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, todo, chatbot
from app.db.mongodb import connect_to_mongo, close_mongo_connection
# khởi tạo fast API 
app = FastAPI(
    title="Todo API",
    description="A Todo application with AI-powered chatbot",
    version="1.0.0"
)

# CORS middleware để frontend goi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers cho phép khi ứng dụng khởi động và tắt
@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

# Include routers vào ứng dụng
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(todo.router, prefix="/api/todos", tags=["Todos"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Welcome to Todo API"}
# trạng thái sức khỏe của API
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
