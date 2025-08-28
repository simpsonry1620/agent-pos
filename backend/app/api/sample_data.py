"""
API endpoints for managing sample data for testing and development
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db_session
from app.models import Account, Hierarchy, CustomerNameAlias, Vendor, Transaction


# Create router
router = APIRouter(prefix="/sample-data", tags=["sample-data"])


@router.post("/create-sample-accounts")
async def create_sample_accounts(db: Session = Depends(get_db_session)):
    """
    Create sample account data for testing fuzzy search functionality.
    
    This creates realistic military and government accounts with various aliases
    to demonstrate the fuzzy matching capabilities.
    """
    try:
        # Check if we already have sample data
        existing_accounts = db.query(Account).count()
        if existing_accounts > 0:
            return {
                "message": "Sample data already exists",
                "existing_accounts": existing_accounts,
                "action": "skipped"
            }
        
        # Create sample hierarchies
        us_public_sector = Hierarchy(
            level_1="US Public Sector",
            level_2="US Federal Government", 
            level_3="Department of Defense",
            level_4="United States Navy"
        )
        
        us_federal_dod = Hierarchy(
            level_1="US Public Sector",
            level_2="US Federal Government",
            level_3="Department of Defense",
            level_4="United States Air Force"
        )
        
        us_federal_dhs = Hierarchy(
            level_1="US Public Sector", 
            level_2="US Federal Government",
            level_3="Department of Homeland Security",
            level_4="Transportation Security Administration"
        )
        
        commercial_defense = Hierarchy(
            level_1="Commercial",
            level_2="Defense Contractors", 
            level_3="Prime Contractors",
            level_4="Lockheed Martin Corporation"
        )
        
        db.add_all([us_public_sector, us_federal_dod, us_federal_dhs, commercial_defense])
        db.commit()
        
        # Create sample accounts
        accounts = [
            Account(
                account_name="United States Navy",
                hierarchy_id=us_public_sector.hierarchy_id,
                account_type="Government",
                url="https://www.navy.mil",
                products="Naval operations, maritime security",
                capabilities="Global naval power projection",
                use_cases="National defense, humanitarian missions",
                primary_industry="Defense",
                industries_served=["Defense", "Maritime Security"]
            ),
            Account(
                account_name="United States Air Force", 
                hierarchy_id=us_federal_dod.hierarchy_id,
                account_type="Government",
                url="https://www.af.mil",
                products="Air and space operations",
                capabilities="Global air superiority, space operations",
                use_cases="Air defense, space missions, cyber warfare",
                primary_industry="Defense",
                industries_served=["Defense", "Aerospace", "Cyber Security"]
            ),
            Account(
                account_name="Transportation Security Administration",
                hierarchy_id=us_federal_dhs.hierarchy_id,
                account_type="Government",
                url="https://www.tsa.gov",
                products="Transportation security services",
                capabilities="Airport security, transportation screening",
                use_cases="Airport security, transportation safety",
                primary_industry="Transportation Security",
                industries_served=["Transportation", "Security", "Aviation"]
            ),
            Account(
                account_name="Lockheed Martin Corporation",
                hierarchy_id=commercial_defense.hierarchy_id,
                account_type="Defense Vendor",
                url="https://www.lockheedmartin.com",
                products="Aerospace, defense, arms, information technology",
                capabilities="Advanced technology systems, mission-critical solutions",
                use_cases="Defense systems, aerospace technology, IT services",
                primary_industry="Defense Technology",
                industries_served=["Defense", "Aerospace", "Technology", "Government Services"]
            )
        ]
        
        db.add_all(accounts)
        db.commit()
        
        # Create customer name aliases for testing fuzzy search
        aliases = [
            # Navy aliases
            CustomerNameAlias(raw_name="USN", account_id=accounts[0].account_id),
            CustomerNameAlias(raw_name="US Navy", account_id=accounts[0].account_id),
            CustomerNameAlias(raw_name="CVN74", account_id=accounts[0].account_id),  # USS John C. Stennis
            CustomerNameAlias(raw_name="NAVSEA", account_id=accounts[0].account_id),
            CustomerNameAlias(raw_name="Naval Sea Systems Command", account_id=accounts[0].account_id),
            CustomerNameAlias(raw_name="NAVAIR", account_id=accounts[0].account_id),
            
            # Air Force aliases
            CustomerNameAlias(raw_name="USAF", account_id=accounts[1].account_id),
            CustomerNameAlias(raw_name="US Air Force", account_id=accounts[1].account_id),
            CustomerNameAlias(raw_name="AFSPC", account_id=accounts[1].account_id),
            CustomerNameAlias(raw_name="Air Force Space Command", account_id=accounts[1].account_id),
            
            # TSA aliases
            CustomerNameAlias(raw_name="TSA", account_id=accounts[2].account_id),
            CustomerNameAlias(raw_name="Transport Security Admin", account_id=accounts[2].account_id),
            
            # Lockheed aliases
            CustomerNameAlias(raw_name="LMT", account_id=accounts[3].account_id),
            CustomerNameAlias(raw_name="Lockheed", account_id=accounts[3].account_id),
            CustomerNameAlias(raw_name="LM", account_id=accounts[3].account_id),
            CustomerNameAlias(raw_name="Lockheed Martin Corp", account_id=accounts[3].account_id)
        ]
        
        db.add_all(aliases)
        db.commit()
        
        return {
            "message": "Sample data created successfully",
            "accounts_created": len(accounts),
            "aliases_created": len(aliases),
            "hierarchies_created": 4,
            "action": "created"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create sample data: {str(e)}")


@router.delete("/clear-all-data")
async def clear_all_data(db: Session = Depends(get_db_session)):
    """
    Clear all data from database (for development/testing only).
    WARNING: This will delete ALL data in the database!
    """
    try:
        # Delete in correct order due to foreign key constraints
        db.query(Transaction).delete()
        db.query(CustomerNameAlias).delete() 
        db.query(Account).delete()
        db.query(Hierarchy).delete()
        db.query(Vendor).delete()
        
        db.commit()
        
        return {
            "message": "All data cleared successfully",
            "action": "cleared"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear data: {str(e)}")


@router.get("/status")
async def get_data_status(db: Session = Depends(get_db_session)):
    """Get current status of sample data in the database"""
    try:
        return {
            "accounts": db.query(Account).count(),
            "hierarchies": db.query(Hierarchy).count(),
            "aliases": db.query(CustomerNameAlias).count(),
            "vendors": db.query(Vendor).count(),
            "transactions": db.query(Transaction).count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data status: {str(e)}")
