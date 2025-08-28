"""
FastAPI main application entry point for AI-Powered POS Account Hierarchy Tool
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered POS Account Hierarchy API",
    description="Autonomous agent for processing inconsistent customer names into structured account hierarchies",
    version="0.1.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
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
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "backend",
        "database": "not_connected"  # Will update when DB connection is added
    }
