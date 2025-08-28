# Backend - FastAPI Application

This directory contains the FastAPI backend for the AI-Powered POS Account Hierarchy & Reporting Tool.

## Structure (Planned)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── accounts.py
│   │   ├── transactions.py
│   │   └── agents.py
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   └── reports.py
│   ├── services/            # Business logic and AI agent services
│   │   ├── __init__.py
│   │   ├── agent.py         # Main AI classification agent
│   │   ├── fuzzy_search.py  # Internal similarity matching
│   │   ├── perplexity.py    # Perplexity API integration
│   │   └── llm_client.py    # NVIDIA LLM client
│   ├── database/            # Database connection and migrations
│   │   ├── __init__.py
│   │   └── connection.py
│   └── config.py            # Configuration and environment variables
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── Dockerfile
└── README.md               # This file
```

## Key Components

### AI Classification Agent Workflow
1. **Fuzzy Search:** Internal similarity matching against existing accounts
2. **Web Research:** Perplexity API for entity research when no match found
3. **Classification:** Local NVIDIA LLM for structuring and categorization
4. **Database Commit:** Autonomous creation of accounts, hierarchies, and aliases

### API Endpoints (Planned)
- `POST /upload/pos` - Upload and process POS Excel files
- `GET /health` - Health check
- `GET /accounts` - List classified accounts
- `GET /reports/account/{account_id}` - Account team reporting
- `GET /reports/vendor/{vendor_id}` - Partner team reporting
- `GET /reports/hierarchy/{level}` - Executive roll-up reporting

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `PERPLEXITY_API_KEY` - Perplexity API key for web research
- `NVIDIA_LLM_URL` - NVIDIA LLM endpoint URL
- `NVIDIA_API_KEY` - NVIDIA API key
