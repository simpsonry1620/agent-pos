"""
Fuzzy search service for matching customer names using PostgreSQL trigram similarity.

This is Step A of the AI Classification Agent workflow - internal fuzzy search
to avoid expensive API calls when we already have the account in our database.
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.models import Account, CustomerNameAlias
from app.config import settings


@dataclass
class FuzzyMatchResult:
    """Result of a fuzzy search operation"""
    account_id: int
    account_name: str
    matched_text: str  # The text that was matched (account name or alias)
    similarity_score: float
    match_type: str  # 'account_name' or 'alias'
    confidence_level: str  # 'high', 'medium', 'low'


class FuzzySearchService:
    """Service for performing fuzzy text matching on customer names"""
    
    def __init__(self, db_session: Session, confidence_threshold: float = None):
        """
        Initialize fuzzy search service
        
        Args:
            db_session: SQLAlchemy database session
            confidence_threshold: Minimum similarity score for high-confidence matches
        """
        self.db = db_session
        self.confidence_threshold = confidence_threshold or settings.fuzzy_match_threshold
    
    def find_best_match(self, raw_customer_name: str) -> Optional[FuzzyMatchResult]:
        """
        Find the best matching account for a raw customer name.
        
        This is the main method used by the AI agent to check if a customer
        already exists before doing web research.
        
        Args:
            raw_customer_name: The raw customer name from POS data (e.g., "USN", "CVN74")
            
        Returns:
            FuzzyMatchResult if a high-confidence match is found, None otherwise
        """
        if not raw_customer_name or len(raw_customer_name.strip()) < 2:
            return None
            
        # Clean the input
        cleaned_name = raw_customer_name.strip()
        
        # Search both account names and aliases
        account_matches = self._search_account_names(cleaned_name)
        alias_matches = self._search_aliases(cleaned_name)
        
        # Combine and find the best match
        all_matches = account_matches + alias_matches
        if not all_matches:
            return None
            
        # Sort by similarity score (highest first)
        best_match = max(all_matches, key=lambda x: x.similarity_score)
        
        # Only return if it meets the confidence threshold
        if best_match.similarity_score >= self.confidence_threshold:
            return best_match
            
        return None
    
    def find_all_matches(self, raw_customer_name: str, limit: int = 10) -> List[FuzzyMatchResult]:
        """
        Find all potential matches for debugging/admin purposes.
        
        Args:
            raw_customer_name: The raw customer name to search for
            limit: Maximum number of results to return
            
        Returns:
            List of FuzzyMatchResult objects sorted by similarity score
        """
        if not raw_customer_name or len(raw_customer_name.strip()) < 2:
            return []
            
        cleaned_name = raw_customer_name.strip()
        
        # Search both account names and aliases
        account_matches = self._search_account_names(cleaned_name, limit)
        alias_matches = self._search_aliases(cleaned_name, limit)
        
        # Combine, sort, and limit results
        all_matches = account_matches + alias_matches
        all_matches.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return all_matches[:limit]
    
    def _search_account_names(self, search_term: str, limit: int = 5) -> List[FuzzyMatchResult]:
        """Search for matches in the accounts table using account names"""
        try:
            # Use PostgreSQL trigram similarity with GIN index
            query = text("""
                SELECT 
                    a.account_id,
                    a.account_name,
                    similarity(a.account_name, :search_term) as sim_score
                FROM accounts a
                WHERE a.account_name % :search_term
                ORDER BY sim_score DESC
                LIMIT :limit
            """)
            
            results = self.db.execute(query, {
                'search_term': search_term,
                'limit': limit
            }).fetchall()
            
            matches = []
            for row in results:
                confidence = self._determine_confidence_level(row.sim_score)
                matches.append(FuzzyMatchResult(
                    account_id=row.account_id,
                    account_name=row.account_name,
                    matched_text=row.account_name,
                    similarity_score=float(row.sim_score),
                    match_type='account_name',
                    confidence_level=confidence
                ))
            
            return matches
            
        except Exception as e:
            # Log the error but don't crash the agent
            print(f"Error in account name fuzzy search: {e}")
            return []
    
    def _search_aliases(self, search_term: str, limit: int = 5) -> List[FuzzyMatchResult]:
        """Search for matches in the customer name aliases table"""
        try:
            # Search aliases and join with accounts to get account info
            query = text("""
                SELECT 
                    a.account_id,
                    a.account_name,
                    c.raw_name as matched_alias,
                    similarity(c.raw_name, :search_term) as sim_score
                FROM customer_name_aliases c
                JOIN accounts a ON c.account_id = a.account_id
                WHERE c.raw_name % :search_term
                ORDER BY sim_score DESC
                LIMIT :limit
            """)
            
            results = self.db.execute(query, {
                'search_term': search_term,
                'limit': limit
            }).fetchall()
            
            matches = []
            for row in results:
                confidence = self._determine_confidence_level(row.sim_score)
                matches.append(FuzzyMatchResult(
                    account_id=row.account_id,
                    account_name=row.account_name,
                    matched_text=row.matched_alias,
                    similarity_score=float(row.sim_score),
                    match_type='alias',
                    confidence_level=confidence
                ))
            
            return matches
            
        except Exception as e:
            print(f"Error in alias fuzzy search: {e}")
            return []
    
    def _determine_confidence_level(self, similarity_score: float) -> str:
        """Determine confidence level based on similarity score"""
        if similarity_score >= 0.8:
            return 'high'
        elif similarity_score >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def is_high_confidence_match(self, similarity_score: float) -> bool:
        """Check if a similarity score represents a high-confidence match"""
        return similarity_score >= self.confidence_threshold
    
    def test_trigram_support(self) -> bool:
        """Test if pg_trgm extension is working properly"""
        try:
            result = self.db.execute(text("""
                SELECT similarity('test', 'testing') as sim_score
            """)).scalar()
            return result is not None and 0 <= result <= 1
        except Exception:
            return False
