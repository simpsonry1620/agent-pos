# **PRD: AI-Powered POS Account Hierarchy & Reporting Tool**

* **Version:** 1.2  
* **Status:** Scoping  
* **Date:** 2025-08-27  
* **Author:** Gemini AI

## **1\. Introduction & Problem Statement 🎯**

Our team receives monthly Point of Sale (POS) reports from various distribution partners. A significant challenge is that the "End Customer Name" field is inconsistent and lacks a standardized, hierarchical structure. For example, the "United States Navy" might appear as "US Navy," "USN," or a specific command like "CVN74." This inconsistency makes it impossible to perform accurate account-level reporting, track sales into key accounts, or understand partner performance within those accounts.

This project aims to build a web application that ingests these POS reports, uses an **AI Agent** to autonomously research and classify end customers into a clean, multi-level hierarchy, and provides powerful, role-based reporting for our account and partner management teams.

## **2\. Goals & Objectives**

* **Primary Goal:** To automate the consolidation and classification of raw POS data into a structured, hierarchical account database.  
* **Secondary Goal:** To provide intuitive, actionable reports for account managers, partner managers, and executives.  
* **Business Objective:** Dramatically reduce the manual effort required for monthly reporting (from days to hours), improve sales data accuracy, and provide deeper insights into account penetration and partner sales patterns.  
* **Technical Objective:** To build a robust application that showcases advanced **AI Agentic behavior**, leveraging a cost-effective combination of local LLMs and targeted web research APIs.

## **3\. User Personas 👥**

* **Sarah, the Navy Account Manager:** Needs to see all sales related to the US Navy, regardless of how the customer is named in the POS file. She wants to see which sub-commands are buying and which vendors (e.g., Lockheed Martin) are selling into her account.  
* **David, the Partner Business Manager:** Manages the relationship with World Wide Technology (WWT). He needs a report showing *only* WWT's sales, broken down by the cleaned, hierarchical end-customer accounts (e.g., how much did WWT sell into the Department of Defense vs. Ford Motor Company).  
* **Maria, the VP of Public Sector Sales:** Needs high-level, roll-up reports. She wants to see total sales for the "US Federal Government" or the entire "US Public Sector" with a single click.

## **4\. Core Features & Functionality (Phase 1\)**

### **Feature 1: Data Ingestion & AI Classification Engine 🤖**

This is the core of the application, driven by an autonomous AI agent workflow.

#### **Workflow for a New POS Report Ingestion:**

1. **File Upload:** A user uploads the monthly POS report (Excel format) via the web UI.  
2. **Row Processing:** The backend processes each row of the report. For each transaction, it extracts the End Customer Name.  
3. **Customer Lookup:** The system checks if a classified parent Account for the End Customer Name already exists in the database.  
4. **Existing Customer Path:** If a match is found, a new Transaction record is created and linked to the existing Account, Vendor, and Parent Account records. The process moves to the next row.  
5. **New Customer Path (Trigger AI Agent):** If no confident match is found, the End Customer Name is sent to the **AI Classification Agent**.

#### **AI Classification Agent Workflow (Fully Autonomous):**

The agent's goal is to determine the correct parent Account and Hierarchy for the new name and commit it to the database.

* **Step A: Internal Fuzzy Search:** The agent first performs a fuzzy search (e.g., using trigram similarity) against the existing Accounts table in the database. If a high-confidence match is found (e.g., "USN" vs. "US Navy"), it proceeds directly to **Step D**, linking the alias to the existing account.  
* **Step B: Web Research (Perplexity API):** If no high-confidence internal match exists, the agent invokes the **Perplexity API** to research the entity. This is the only step that incurs a per-token cost and should be used judiciously. The agent will query for:  
  * Official URL  
  * Products & Capabilities  
  * Primary Industry / Customer Base  
  * Other Industries Served  
  * Potential parent organizations (e.g., research on "CVN74" should reveal it's part of the US Navy).  
* **Step C: Classification & Structuring (Local LLM):** The structured output from Perplexity is fed to a powerful **local LLM** via an OpenAI-compatible endpoint. The local LLM's task is to:  
  * Synthesize the research data.  
  * Determine the correct parent Account name (e.g., "United States Navy").  
  * Propose the full hierarchy (e.g., United States Navy \-\> Department of Defense \-\> US Federal Government \-\> US Public Sector).  
  * Classify the entity type (e.g., Government Agency, Defense Vendor, ISV, Automotive).  
  * Extract and structure the researched data (URL, industries, etc.) into a clean JSON object for database insertion.  
* **Step D: Autonomous Database Commit:** The agent autonomously commits its findings. It creates the new Account, establishes the Hierarchy, creates the CustomerNameAlias link, and inserts the initial Transaction record. A detailed log of the agent's actions, including the Perplexity data and LLM output, will be stored for auditing purposes.

### **Feature 2: Reporting & Analytics Dashboard 📊**

A simple, clean, and responsive web interface for viewing reports.

* **Account Team View:**  
  * Filterable by Parent Account (e.g., "United States Navy").  
  * Displays all transactions rolling up to that account, including those from sub-agencies.  
  * Shows a breakdown of sales by Vendor within that account.  
  * Data visualization of sales over time.  
* **Partner (Vendor) Team View:**  
  * Filterable by Vendor (e.g., "World Wide Technology").  
  * Displays all sales for that partner, aggregated by the classified Parent Account.  
  * Allows drill-down to see which specific sub-agencies their sales went to.  
* **Executive Roll-up View:**  
  * Provides high-level views based on the hierarchy (e.g., "US Public Sector", "US Federal Government", "Financial Services").  
  * Top-level KPIs and visualizations of performance across major sectors.

## **5\. Technical Architecture & Stack**

* **Frontend:** **React (Vite) or Vue.js**. Should be a responsive single-page application (SPA) that can be viewed on both desktop and mobile.  
* **Backend:** **Python** with **FastAPI**. Ideal for its speed, ease of use, and excellent support for AI/ML libraries.  
* **Database:** **PostgreSQL**. It's robust, open-source, and has excellent extensions like pg\_trgm for efficient fuzzy text searching.  
* **AI & LLM Integration:**  
  * **Local LLMs:** Accessed via a stable, **OpenAI-compatible API endpoint** on the LAN. This will handle all classification, summarization, and data structuring tasks to minimize cost.  
  * **Perplexity API:** Used *only* for the web research step within the AI agent workflow. The API key will be stored securely in the backend configuration.  
  * **AI Agent Orchestration:** Use a library like **LangChain** or build a simple state machine in Python to manage the steps of the classification workflow.

### **Proposed Database Schema (Simplified)**

\-- Stores the cleaned, parent-level account names  
CREATE TABLE Accounts (  
    account\_id SERIAL PRIMARY KEY,  
    account\_name VARCHAR(255) UNIQUE NOT NULL, \-- e.g., 'United States Navy'  
    hierarchy\_id INT REFERENCES Hierarchies(hierarchy\_id),  
    account\_type VARCHAR(100), \-- 'Government', 'Defense Vendor', 'ISV'  
    url TEXT,  
    products TEXT,  
    capabilities TEXT,  
    use\_cases TEXT,  
    primary\_industry VARCHAR(255),  
    industries\_served TEXT\[\],  
    created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP  
);

\-- Stores the many-to-one raw names found in POS reports  
CREATE TABLE CustomerNameAliases (  
    alias\_id SERIAL PRIMARY KEY,  
    raw\_name VARCHAR(255) UNIQUE NOT NULL, \-- e.g., 'CVN74', 'USN'  
    account\_id INT REFERENCES Accounts(account\_id) NOT NULL  
);

\-- Defines the hierarchical structure  
CREATE TABLE Hierarchies (  
    hierarchy\_id SERIAL PRIMARY KEY,  
    level\_1 VARCHAR(255), \-- e.g., 'US Public Sector'  
    level\_2 VARCHAR(255), \-- e.g., 'US Federal Government'  
    level\_3 VARCHAR(255), \-- e.g., 'Department of Defense'  
    level\_4 VARCHAR(255)  \-- e.g., 'United States Navy'  
);

\-- Stores info about distribution partners/vendors  
CREATE TABLE Vendors (  
    vendor\_id SERIAL PRIMARY KEY,  
    vendor\_name VARCHAR(255) UNIQUE NOT NULL,  
    partner\_business\_manager VARCHAR(255),  
    salesforce\_link TEXT  
);

\-- Stores individual transaction line items from POS reports  
CREATE TABLE Transactions (  
    transaction\_id SERIAL PRIMARY KEY,  
    pos\_report\_id INT, \-- To link back to a specific uploaded file  
    transaction\_date DATE,  
    product\_sku VARCHAR(100),  
    quantity INT,  
    sale\_amount NUMERIC(12, 2),  
    account\_id INT REFERENCES Accounts(account\_id),  
    vendor\_id INT REFERENCES Vendors(vendor\_id),  
    original\_customer\_name VARCHAR(255) \-- Store the raw name for auditing  
);

\-- Stores a log of the AI agent's actions for auditing  
CREATE TABLE AgentLogs (  
    log\_id SERIAL PRIMARY KEY,  
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,  
    raw\_name\_processed VARCHAR(255),  
    action\_taken VARCHAR(100), \-- e.g., 'CREATED\_NEW\_ACCOUNT', 'MATCHED\_EXISTING\_ALIAS'  
    resulting\_account\_id INT REFERENCES Accounts(account\_id),  
    confidence\_score FLOAT,  
    llm\_output JSONB,  
    perplexity\_data JSONB  
);

## **6\. Development Environment & Deployment 🐳**

To ensure a consistent and easy-to-manage development environment for all team members, this project will use **Docker Compose**. It allows us to define and run the entire multi-container application (backend, frontend, database) with a single command. This approach isolates dependencies and eliminates "it works on my machine" issues.

### **Sample docker-compose.yml**

This file should be placed in the root of the project repository.

version: '3.8'

services:  
  \# Backend FastAPI Service  
  backend:  
    build: ./backend \# Path to the backend Dockerfile  
    ports:  
      \- "8000:8000" \# Map host port 8000 to container port 8000  
    volumes:  
      \- ./backend:/app \# Mount backend code for live reloading  
    environment:  
      \- DATABASE\_URL=postgresql://user:password@db:5432/pos\_data  
      \# Add other env vars like API keys here  
    depends\_on:  
      \- db \# Ensures the database is started before the backend  
    networks:  
      \- app-network

  \# Frontend React/Vue Service  
  frontend:  
    build: ./frontend \# Path to the frontend Dockerfile  
    ports:  
      \- "3000:3000" \# Map host port 3000 to container port 3000  
    volumes:  
      \- ./frontend/src:/app/src \# Mount src for live reloading  
    networks:  
      \- app-network

  \# PostgreSQL Database Service  
  db:  
    image: postgres:15-alpine  
    volumes:  
      \- postgres\_data:/var/lib/postgresql/data/ \# Persist data  
    environment:  
      \- POSTGRES\_USER=user  
      \- POSTGRES\_PASSWORD=password  
      \- POSTGRES\_DB=pos\_data  
    ports:  
      \- "5432:5432" \# Expose DB port for local inspection (optional)  
    networks:  
      \- app-network

networks:  
  app-network:  
    driver: bridge

volumes:  
  postgres\_data: \# Define the named volume for data persistence

## **7\. Phase 2 & Future Considerations**

The initial design should be flexible to accommodate future features:

* **Semantic Search:** The use\_cases and capabilities fields in the Accounts table should be populated by the AI agent in Phase 1\. This will provide the foundational data for a future semantic search feature to find customers with specific needs.  
* **MCP (Managed Cloud Provider) Analysis:** We can add a tag or field in the Accounts table to track MCP status, allowing for more advanced reporting later.  
* **Authentication:** While not needed for the LAN-based initial version, using a framework that easily supports adding authentication (like FastAPI with OAuth2) is wise.  
* **UI for Manual Correction:** After the initial bulk processing, a simple UI for admins to correct any misclassifications made by the agent will be valuable.

## **8\. Getting Started for Cursor**

1. **Project Setup:** Initialize a monorepo with a frontend (React/Vite) directory and a backend (FastAPI) directory. Place the docker-compose.yml file in the root.  
2. **Backend First:**  
   * Focus on setting up the PostgreSQL database schema using an ORM like SQLAlchemy.  
   * Build the basic FastAPI endpoints for file upload (/upload/pos).  
   * Develop the autonomous AI agent workflow as a series of services/functions. Start with the "happy path" where a customer already exists. Then, build out the agentic chain: fuzzy\_search \-\> perplexity\_call \-\> local\_llm\_classify \-\> database\_commit.  
3. **Frontend Second:**  
   * Build the file upload component.  
   * Develop one of the report views (e.g., the Account Team View) to prove out the data model and provide immediate value.  
   * The "Review Queue" is no longer needed for Phase 1\.