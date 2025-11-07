from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.attendance.routes import router as attendance_router
from app.admin.routes import router as admin_router

# Create FastAPI app
app = FastAPI(
    title="Smart Attendance System API",
    description="A FastAPI backend for Smart Attendance System with face recognition",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(attendance_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart Attendance System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Smart Attendance System API is running"
    }