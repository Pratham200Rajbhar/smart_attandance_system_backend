from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import Base, engine
from app.auth.routes import auth_router
from app.admin.routes import admin_router

app = FastAPI(
    title="Simple CRUD API", 
    version="1.0.0",
    description="A simplified backend API with basic CRUD operations and authentication"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {
        "message": "Simple CRUD API", 
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
@app.get("/")
async def root():
    return {"message": "Smart Attendance System API", "status": "running"}
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
