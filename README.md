# AI-Powered POS Account Hierarchy & Reporting Tool

An autonomous AI agent system that processes Point of Sale (POS) reports, classifies inconsistent customer names into structured account hierarchies, and provides powerful reporting dashboards.

## Project Structure

```
agent-pos/
├── backend/           # FastAPI application
├── frontend/          # React (Vite) application  
├── docker-compose.yml # Development environment
├── PRD.md            # Product Requirements Document
├── TODO-Implementation.md # Implementation checklist
└── README.md         # This file
```

## Quick Start

1. **Prerequisites:**
   - Docker and Docker Compose
   - Git

2. **Development Setup:**
   ```bash
   # Clone and navigate to project
   cd agent-pos
   
   # Start all services
   docker compose up --build
   ```

3. **Access the Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:5432

## Key Features

- **AI Classification Agent:** Autonomous research and classification of customer names
- **Account Hierarchy Management:** Multi-level account structure (Public Sector → Federal → DoD → Navy)
- **Role-based Reporting:** Account managers, partner managers, and executive views
- **Fuzzy Matching:** Intelligent linking of similar customer name variants
- **Audit Logging:** Complete trail of AI agent decisions

## Technology Stack

- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** React, Vite, TypeScript
- **AI Integration:** Local NVIDIA LLM + Perplexity API
- **Development:** Docker Compose

## Development Status

This project is currently in development. See `TODO-Implementation.md` for the current implementation roadmap.
