"""
API endpoints for fuzzy search functionality
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db_session
from app.services.fuzzy_search import FuzzySearchService, FuzzyMatchResult


# Pydantic models for API responses
class FuzzyMatchResponse(BaseModel):
    account_id: int
    account_name: str
    matched_text: str
    similarity_score: float
    match_type: str
    confidence_level: str


class FuzzySearchTestResponse(BaseModel):
    query: str
    best_match: Optional[FuzzyMatchResponse]
    all_matches: List[FuzzyMatchResponse]
    total_matches: int
    high_confidence_match: bool


# Create router
router = APIRouter(prefix="/fuzzy-search", tags=["fuzzy-search"])


@router.get("/test", response_model=FuzzySearchTestResponse)
async def test_fuzzy_search(
    query: str = Query(..., description="Customer name to search for", min_length=1),
    show_all: bool = Query(default=False, description="Show all matches, not just best match"),
    limit: int = Query(default=10, description="Maximum number of matches to return", ge=1, le=50),
    db: Session = Depends(get_db_session)
):
    """
    Test fuzzy search functionality by searching for customer name matches.
    
    This endpoint is used for development and testing of the fuzzy search capabilities
    that power Step A of the AI Classification Agent workflow.
    """
    try:
        fuzzy_service = FuzzySearchService(db)
        
        # Get the best match (high-confidence only)
        best_match = fuzzy_service.find_best_match(query)
        
        # Get all matches for analysis (if requested)
        all_matches = fuzzy_service.find_all_matches(query, limit) if show_all else []
        
        return FuzzySearchTestResponse(
            query=query,
            best_match=FuzzyMatchResponse(**best_match.__dict__) if best_match else None,
            all_matches=[FuzzyMatchResponse(**match.__dict__) for match in all_matches],
            total_matches=len(all_matches),
            high_confidence_match=best_match is not None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fuzzy search failed: {str(e)}")


@router.get("/health")
async def fuzzy_search_health(db: Session = Depends(get_db_session)):
    """Check if fuzzy search functionality is working"""
    try:
        fuzzy_service = FuzzySearchService(db)
        trigram_working = fuzzy_service.test_trigram_support()
        
        return {
            "status": "healthy" if trigram_working else "error",
            "pg_trgm_working": trigram_working,
            "confidence_threshold": fuzzy_service.confidence_threshold,
            "service": "FuzzySearchService"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.post("/batch-test")
async def batch_fuzzy_test(
    queries: List[str],
    db: Session = Depends(get_db_session)
):
    """
    Test multiple customer names at once for bulk analysis.
    Useful for testing the fuzzy search with known customer name variations.
    """
    if len(queries) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 queries allowed per batch")
        
    try:
        fuzzy_service = FuzzySearchService(db)
        results = {}
        
        for query in queries:
            if query.strip():
                best_match = fuzzy_service.find_best_match(query.strip())
                results[query] = {
                    "match_found": best_match is not None,
                    "match": FuzzyMatchResponse(**best_match.__dict__) if best_match else None
                }
        
        return {
            "batch_results": results,
            "total_queries": len(queries),
            "matches_found": sum(1 for r in results.values() if r["match_found"])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch test failed: {str(e)}")
