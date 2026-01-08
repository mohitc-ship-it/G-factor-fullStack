# Problem Statement

Manufacturing plants in chemical processing and surface finishing rely heavily on manual monitoring, manual data entry, and operator expertise for troubleshooting.  

Key challenges include:

- Operators manually search across log sheets, analytical methods, manuals, and historical troubleshooting reports.
- Process deviations (temperature, current, chemistry imbalance) are detected late.
- Analytical data and instrument readings are stored in different formats and locations.
- Troubleshooting knowledge is lost when senior engineers leave.
- No unified system exists to centralize data, detect anomalies, and provide AI-powered root-cause guidance.

**GFacture AI** solves these problems by providing a unified, intelligent, and data-driven platform.

---

# Approach

1. **Centralize All Data**
   - PLC/process data (simulated for MVP)
   - Analytical lab results
   - Analytical instrument readings
   - Manuals, SOPs, methods, technical reports
   - Troubleshooting records

2. **Apply AI Intelligence**
   - Detect anomalies based on rules + historical patterns
   - Generate warnings and corrective suggestions
   - Extract knowledge from internal documents
   - Search approved external troubleshooting websites
   - Provide conversational AI assistance

3. **Build a 4-Module MVP**
   - **Dashboard:** Process data, analytical data, AI alerts
   - **Knowledge Base:** Searchable documents
   - **Analytics:** Historical alerts & troubleshooting
   - **AI Assistant:** Internal + approved external website search

4. **Implement Rule Engine**
   - User-defined acceptable ranges
   - Chemistry thresholds
   - Automatic anomaly detection

5. **Prepare for Future IoT**
   - MVP uses input data only
   - Future phases will integrate PLCs and instruments via IoT devices

---

# Technical Architecture

┌──────────────────────────────────────────┐
│ Frontend │
│ - Next.js (Dashboard, KB, Analytics) │
│ - AI Assistant UI │
└───────────────────────────┬──────────────┘
│
▼
┌──────────────────────────────────────────┐
│ Data Ingestion Layer │
│ - Upload log sheets │
│ - Input analytical data │
│ - Input instrument readings │
│ - Upload troubleshooting reports │
└───────────────────────────┬──────────────┘
│
▼
┌──────────────────────────────────────────┐
│ Rule Engine & Validator │
│ - Acceptable ranges │
│ - Threshold detection │
│ - User-defined rules │
│ - Anomaly detection │
└───────────────────────────┬──────────────┘
│
▼
┌──────────────────────────────────────────┐
│ AI Layer │
│ - Document parsing (PDF/Word/Excel) │
│ - Vector search (internal docs) │
│ - External website search (approved) │
│ - AI troubleshooting engine │
└───────────────────────────┬──────────────┘
│
▼
┌──────────────────────────────────────────┐
│ Database │
│ - Logs, alerts, rules │
│ - Analytical records │
│ - Troubleshooting history │
│ - Document metadata │
└──────────────────────────────────────────┘



---

# Tech Stack

### Frontend
- Next.js (React + TypeScript)  
- TailwindCSS 
- Recharts or Chart.js for analytics  

### AI & NLP
- Python backend (optional FastAPI)
- LangChain  
- OpenAI GPT-4 / GPT-4o
- GraphRAG   
- Custom Crawler (Playwright MCP)  



### Hosting
- Vercel  

---

