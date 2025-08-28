# **Implementation To-Do List: AI POS Automation**

This to-do list breaks down the development work for the AI-Powered POS Account Hierarchy & Reporting Tool, based on PRD version 1.2.

## **Phase 1: Project Setup & Backend Foundation**

This phase focuses on creating the project structure, development environment, and database schema.

* \[ \] **Project Scaffolding:**  
  * \[ \] Initialize a new monorepo.  
  * \[ \] Create a backend directory for the FastAPI application.  
  * \[ \] Create a frontend directory for the React application.  
  * \[ \] Add a .gitignore file to the root.  
* \[ \] **Docker Environment:**  
  * \[ \] Create the docker-compose.yml file in the project root as defined in the PRD.  
  * \[ \] Create a Dockerfile for the backend service.  
  * \[ \] Create a Dockerfile for the frontend service.  
  * \[ \] Create a .env file in the backend directory to store secrets (Database URL, API keys).  
  * \[ \] Run docker-compose up \--build to verify that all services (backend, frontend, db) start correctly.  
* \[ \] **Database & ORM Setup:**  
  * \[ \] In the FastAPI backend, add SQLAlchemy and psycopg2-binary as dependencies.  
  * \[ \] Create Python models using SQLAlchemy that mirror the SQL schema in the PRD (Accounts, CustomerNameAliases, Hierarchies, Vendors, Transactions, AgentLogs).  
  * \[ \] Implement a database connection module that reads the DATABASE\_URL from environment variables.  
  * \[ \] Use a migration tool like Alembic to initialize the database schema.  
* \[ \] **Basic API Endpoints:**  
  * \[ \] Create a health check endpoint (e.g., /health) to confirm the API is running.  
  * \[ \] Create the initial file upload endpoint (POST /upload/pos) that accepts an Excel file. For now, it can just save the file and return a success message.

## **Phase 2: Core AI Agent Implementation**

This phase involves building the autonomous agent logic within the FastAPI backend.

* \[ \] **Internal Fuzzy Search (Step A):**  
  * \[ \] Install the pg\_trgm extension in the PostgreSQL database via an Alembic migration.  
  * \[ \] Create a function that takes a raw customer name and performs a trigram similarity search against the Accounts table.  
  * \[ \] Establish a confidence threshold (e.g., \> 0.6 similarity) to determine a "high-confidence match."  
* \[ \] **Web Research Integration (Step B):**  
  * \[ \] Add a service/module for interacting with the **Perplexity API**.  
  * \[ \] Store the Perplexity API key securely in the .env file.  
  * \[ \] Create a function that takes a customer name, queries the Perplexity API for the required information (URL, capabilities, etc.), and returns structured data.  
* \[ \] **LLM Classification Integration (Step C):**  
  * \[ \] Add a service/module for interacting with your **NVIDIA LLM endpoint**.  
  * \[ \] Store the LLM API URL and nvapikey securely in the .env file.  
  * \[ \] Design a robust prompt that takes the Perplexity research data as context and instructs the LLM to return a JSON object with the final classification (account\_name, hierarchy, account\_type, etc.).  
  * \[ \] Create a function that sends the prompt and context to the LLM and parses the JSON response.  
* \[ \] **Orchestrate the Agent Workflow:**  
  * \[ \] Connect the pieces: fuzzy\_search \-\> perplexity\_call \-\> local\_llm\_classify \-\> database\_commit.  
  * \[ \] Implement the logic to process an uploaded Excel file row by row.  
  * \[ \] For each new customer name, trigger the full agent workflow.  
  * \[ \] Implement the database commit logic (Step D) to create/update Accounts, Hierarchies, CustomerNameAliases, and Transactions.  
  * \[ \] Ensure every agent action is logged to the AgentLogs table for auditing.

## **Phase 3: Frontend Development**

This phase focuses on building the user interface for file uploads and basic data viewing.

* \[ \] **Project Setup (Frontend):**  
  * \[ \] Initialize a new React project using Vite (npm create vite@latest).  
  * \[ \] Install axios for making API calls to the backend.  
  * \[ \] Set up a proxy in the Vite config to forward API requests to the FastAPI backend to avoid CORS issues in development.  
* \[ \] **File Upload Component:**  
  * \[ \] Create a simple UI with a file input that accepts .xlsx and .xls files.  
  * \[ \] Add a button to submit the file to the POST /upload/pos backend endpoint.  
  * \[ \] Implement UI feedback for upload status (e.g., loading spinner, success/error messages).  
* \[ \] **Data Display Components (Initial):**  
  * \[ \] Create a new page/view to display classified accounts.  
  * \[ \] Create a backend endpoint (GET /accounts) to fetch all classified accounts.  
  * \[ \] Build a simple table component in React to display the data from the /accounts endpoint.

## **Phase 4: Reporting & Analytics Dashboard**

This phase involves building the specific reporting views outlined in the PRD.

* \[ \] **Backend Reporting Endpoints:**  
  * \[ \] Create an endpoint for the **Account Team View** (e.g., GET /reports/account/{account\_id}). It should aggregate all relevant transaction data.  
  * \[ \] Create an endpoint for the **Partner Team View** (e.g., GET /reports/vendor/{vendor\_id}).  
  * \[ \] Create an endpoint for the **Executive Roll-up View** (e.g., GET /reports/hierarchy/{level\_name}).  
* \[ \] **Frontend Reporting UI:**  
  * \[ \] Design and build the UI for the **Account Team View**, including filters and data visualizations (e.g., using a library like Recharts or Chart.js).  
  * \[ \] Design and build the UI for the **Partner Team View**.  
  * \[ \] Design and build the UI for the **Executive Roll-up View**.