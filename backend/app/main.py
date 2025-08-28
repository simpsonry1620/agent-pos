"""
FastAPI main application entry point for AI-Powered POS Account Hierarchy Tool
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db_session
from app.models import Account, Hierarchy, Vendor

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered POS Account Hierarchy API",
    description="Autonomous agent for processing inconsistent customer names into structured account hierarchies",
    version="0.1.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI-Powered POS Account Hierarchy API",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db_session)):
    """Health check endpoint with database connectivity test"""
    database_status = "disconnected"
    pg_trgm_status = "unknown"
    
    try:
        # Test basic database connection
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            database_status = "connected"
            
        # Test pg_trgm extension
        extensions = db.execute(text("SELECT extname FROM pg_extension WHERE extname = 'pg_trgm'")).fetchall()
        pg_trgm_status = "enabled" if extensions else "disabled"
        
    except Exception as e:
        database_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "backend",
        "database": database_status,
        "pg_trgm_extension": pg_trgm_status,
        "models_available": True
    }

@app.get("/database/stats")
async def database_stats(db: Session = Depends(get_db_session)):
    """Get database statistics for development/monitoring"""
    try:
        stats = {}
        
        # Count records in each table
        stats["accounts"] = db.query(Account).count()
        stats["hierarchies"] = db.query(Hierarchy).count() 
        stats["vendors"] = db.query(Vendor).count()
        
        return {
            "status": "success",
            "table_counts": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
