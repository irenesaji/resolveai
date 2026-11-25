
# ResolveAI – Intelligent Customer Support & Operations Copilot

ResolveAI is an AI-powered customer support application designed to
help support teams classify, prioritize and respond to customer
complaints.

## Features

- Customer ticket submission and tracking
- AI-powered ticket classification
- Sentiment analysis
- Automatic priority detection
- AI-generated customer response suggestions
- RAG-based knowledge retrieval
- PDF and text document ingestion
- ChromaDB vector storage
- Human review and approval workflow
- Ticket analytics dashboard
- SQLite database integration

## Technology Stack

- Python
- Streamlit
- Google Gemini API
- Gemini Embeddings
- ChromaDB
- SQLite
- Pandas
- PyPDF
- Pytest

## Architecture

1. Customers submit support tickets through Streamlit.
2. Ticket information is stored in SQLite.
3. Gemini analyzes the complaint.
4. The application retrieves relevant knowledge-base documents.
5. Gemini generates a suggested customer response.
6. Analysis results are saved in SQLite.
7. A human support agent reviews the suggestion.
8. Dashboard analytics display ticket information.

## Project Structure

app/
- main.py
- services/gemini_service.py
- services/ticket_analyzer.py
- services/knowledge_base.py

database/
- db.py

data/
- knowledge_base/
- chroma_db/

tests/
- test_db.py

## Installation

Clone the repository:

git clone https://github.com/irenesaji/resolveai.git

Navigate into the project:

cd resolveai

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

Create a .env file:

GEMINI_API_KEY=your_api_key
AI_PROVIDER=gemini

Run the application:

python -m streamlit run app/main.py

## Testing

Run:

python -m pytest -v

## Security

API keys are stored in environment variables.
The .env file must not be committed to GitHub.

## Project Status

Developed as an AI customer-support automation prototype.
