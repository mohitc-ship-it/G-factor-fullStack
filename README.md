# Untostr BBT - Anomaly Insight & Analysis Platform

This repository contains the source code of poc demo built for G-Factor client , a comprehensive solution for analyzing manufacturing reports, detecting anomalies, and providing AI-driven insights. The project is divided into three main components: a Backend service, a Phase 1 Frontend (Anomaly Insight Chat), and a Phase 2 Frontend (Advanced Dashboard).

## Project Structure

```
.
├── anomaly-insight-chat/  # Frontend Phase 1: Initial anomaly detection interface
├── backend/               # Backend API & Multimodal Graph RAG System
└── frontend/              # Frontend Phase 2: Advanced Dashboard & Analytics
```

---

## 1. Backend

The backend is a **FastAPI** application that handles file processing,Multimodal Graph RAG (Retrieval-Augmented Generation) storage, and chat interactions.

### Key Files & Directories

*   **`app.py`**: The main entry point for the API.
    *   **Endpoints**:
        *   `POST /chat`: Accepts a query and returns an AI-generated response using the RAG system.
        *   `POST /upload-reports`: Handles file uploads (PDF, Excel, etc.), converts Excel files to PDF, stores documents in the vector database, and performs initial anomaly analysis.
*   **`ragAnything.py`**: The core RAG implementation.
    *   Uses **LightRAG** and **OpenAI** to index documents and perform hybrid searches.
    *   Manages the vector database storage in `rag_storage3`.
    *   Includes a structured output pipeline to format LLM responses as JSON.
*   **`excel_to_pdf.py`**: Utility script to convert uploaded Excel files into PDF format for consistent processing by the RAG system.
*   **`services.py`**: Contains business logic for analyzing files and detecting anomalies (`analyze_file`, `anamolies_detection`).
*   **`utils.py`**: Helper functions for JSON manipulation and report loading.

### Setup & Usage

1.  Navigate to the `backend` directory.
2.  Install dependencies (e.g., `pip install -r requirements.txt`).
3.  Ensure your `.env` file is configured with the necessary API keys (e.g., `OPENAI_API_KEY`).
4.  Run the server (typically `uvicorn app:app --reload` or `python app.py`).

---

## 2. Frontend Phase 1 (`anomaly-insight-chat`)

This is the initial frontend implementation focused on a project-based workflow for uploading reports and chatting with the insights.

### Key Features

*   **Project Management**: Create and manage separate projects for different sets of reports.
*   **File Upload**: Upload multiple files to a project.
*   **Results Dashboard**: View analyzed reports and detected anomalies.
*   **Floating Chatbot**: A chat interface to ask questions about the uploaded documents.

### Key Files

*   **`src/pages/Index.tsx`**: The main controller component. It manages the state between different views:
    *   `projects`: List of existing projects.
    *   `upload`: File upload interface for new projects.
    *   `results`: The dashboard view for a selected project.
*   **`src/components/FileUpload.tsx`**: Component for handling file selection and upload progress.
*   **`src/components/ResultsDashboard.tsx`**: Displays the analysis results.
*   **`src/components/FloatingChatbot.tsx`**: The chat widget for user interaction.

---

## 3. Frontend Phase 2 (`frontend`)

This folder contains the evolved, feature-rich version of the frontend application, designed as a comprehensive dashboard.

### Key Features

*   **Tabbed Navigation**: Easy access to different modules via a persistent top navigation bar.
*   **Dashboard**: A high-level overview of system status and key metrics.
*   **Knowledge Base**: A repository view of all processed information.
*   **Analytics**: Visualizations and data analysis tools.
*   **AI Assistant**: A dedicated full-page interface for interacting with the AI.
*   **Rules**: Interface for managing anomaly detection rules.

### Key Files

*   **`src/App.tsx`**: The main application layout. It handles the routing/switching between the different tabs (`Dashboard`, `KnowledgeBase`, `Analytics`, `AIAssistant`, `Rules`).
*   **`src/pages/`**: Contains the individual page components:
    *   `Dashboard.tsx`
    *   `KnowledgeBase.tsx`
    *   `Analytics.tsx`
    *   `AIAssistant.tsx`
    *   `Rules.tsx`
*   **`src/components/TabNavigation.tsx`**: The navigation component that controls the active view.

### Setup & Usage

1.  Navigate to the `frontend` directory.
2.  Install dependencies: `npm install` or `bun install`.
3.  Start the development server: `npm run dev` or `bun run dev`.



### Below is full detailed requirement for further MVP building (as per clients interaction)

GFacture AI – MVP Feature Summary
1. Dashboard
* Manufacturing Parts: Add and track part details (name, surface area, reject reason).
* Data from PLC (Simulated will be as per data provided): Manual input of process parameters (T, I, t) for E-Clean, Pickle, Ni Strike, and Ni Sulfamate.
* AI-Generated Alerts: Detect and display warnings or alarms based on rules and historical data.
* Analytical Works:
    * Enter lab analysis data (Free/Total Alkalinity, pH, NiCl₂ concentration, etc.).
    * Automatic alerts (e.g., “Low HCl – add 4 gal”).
* Analytical Instruments:
    * Input readings (Cu, Cr, Fe ppm) from Atomic Absorption Spectrometer.
    * AI detects contamination and gives corrective guidance.
* Troubleshooting & Service Calls:
    * Add problem, root cause, and solution.
    * Upload searchable PDF/Word/Excel files (saved into Knowledge Base).
    * Automatic tagging and indexing for quick access.

2. Knowledge Base
* search manuals, analytical methods, service reports, and troubleshooting PDFs.
* Full-text and semantic search across all internal documents.

3. Analytics
* View history of alerts, anomalies, and troubleshooting by process step.
* Time-range filters (daily / weekly / monthly).
* Example display:History of Alerts and Troubleshooting for the E-Clean Tank containing date, problem , root cause, solution 

4. AI Assistant
* Conversational assistant trained on uploaded data and documents.
* Provides troubleshooting help and root-cause suggestions with references.
* Search Modes:
    * Internal Only – searches company data.
    * Internal + Approved Websites – searches specific client-approved sites for troubleshooting PDFs and solutions.
* Displays sourced answers with document or website citations.
# G-factor-fullStack
