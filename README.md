# ResolveAI – Intelligent Customer Support & Operations Copilot

ResolveAI is an AI-powered customer support application that helps support teams analyze customer complaints, prioritize tickets, retrieve relevant information from company documents, and generate suggested responses.

The application combines Generative AI, Retrieval-Augmented Generation (RAG), and a human-in-the-loop review workflow to support customer service operations.

## Features

- **Customer Ticket Management:** Submit and store customer complaints.
- **AI Ticket Analysis:** Use Google Gemini to classify tickets by category, sentiment, and priority.
- **AI-Generated Responses:** Generate suggested customer replies based on the complaint and relevant knowledge.
- **Knowledge Base:** Upload PDF, TXT, and Markdown documents.
- **Semantic Search:** Retrieve relevant document chunks using embeddings and ChromaDB.
- **Human-in-the-Loop Review:** Allow support agents to approve responses or request changes.
- **Ticket Resolution:** Update ticket status after handling.
- **Dashboard:** View ticket statistics, categories, priorities, and recent tickets.
- **Ticket History:** Review submitted tickets and their analysis.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Generative AI | Google Gemini API |
| Embeddings | Gemini Embedding Model |
| Vector Database | ChromaDB |
| Relational Database | SQLite |
| PDF Processing | pypdf |
| Data Analysis | Pandas |
| Testing | Pytest |
| Version Control | Git and GitHub |

## Project Architecture

```text
Customer
   |
   v
Streamlit Application
   |
   v
Ticket Management
   |
   +------> SQLite Database
   |
   v
AI Ticket Analysis
   |
   +------> Google Gemini
   |
   v
Knowledge Base Retrieval
   |
   +------> Gemini Embeddings
   |
   +------> ChromaDB
   |
   v
Suggested Customer Response
   |
   v
Human Review
   |
   +------> Approve
   |
   +------> Request Changes
   |
   v
Ticket Resolution
```

## How It Works

1. A customer support ticket is submitted through the application.
2. The ticket is stored in the SQLite database.
3. The support agent selects a ticket for AI analysis.
4. ResolveAI searches the uploaded knowledge base for relevant information.
5. Gemini analyzes the complaint using the retrieved context.
6. The AI generates a category, sentiment, priority, and suggested response.
7. A human support agent reviews the generated response.
8. The agent can approve the suggestion, request changes, or mark the ticket as resolved.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/irenesaji/resolveai.git
cd resolveai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit your actual API key to GitHub.

### 5. Run the Application

```bash
python -m streamlit run app/main.py
```

Open the local URL displayed in the terminal.

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The project includes tests for database operations, knowledge base functionality, and AI ticket analysis.

## Project Structure

```text
ResolveAI/
│
├── app/
│   ├── main.py
│   └── services/
│       ├── gemini_service.py
│       ├── knowledge_base.py
│       └── ticket_analyzer.py
│
├── data/
│   └── knowledge_base/
│
├── database/
│   └── db.py
│
├── tests/
│   ├── test_db.py
│   ├── test_knowledge_base.py
│   └── test_ticket_analyzer.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Runtime database and vector-store files are generated locally.

## Important Notes

- A valid Gemini API key is required for AI analysis and embedding generation.
- Uploaded documents should contain extractable text. Scanned PDFs may require OCR.
- AI-generated responses are suggestions and should be reviewed by a human before being sent to customers.
- The sample support policy is for demonstration purposes and is not an official company policy.
- The application is a prototype and does not automatically issue refunds, contact customers, or integrate with a live order-management system.

## Future Improvements

- User authentication and role-based access control.
- Integration with real customer support platforms.
- More advanced ticket analytics and reporting.
- Response quality evaluation.
- Improved document management and OCR support.
- Deployment with production-grade database and security controls.

## Author

**Irene Saji**

GitHub: https://github.com/irenesaji

LinkedIn: https://www.linkedin.com/in/irene-saji12
