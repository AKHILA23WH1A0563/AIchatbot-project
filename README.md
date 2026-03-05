# AI Travel Chatbot with RAG (Complete Implementation)

## Project Overview

A full-stack AI Travel Chatbot with complete RAG (Retrieval-Augmented Generation) implementation. The system uses semantic search with ChromaDB, vector embeddings, and LLM integration to provide accurate travel information from PDF documents.

**Tech Stack:**
- **Backend**: FastAPI, MongoDB, ChromaDB, LangChain, Groq LLM
- **Frontend**: React, JavaScript, CSS
- **AI/ML**: Sentence Transformers, Semantic Search, RAG Pipeline

---

## Project Structure

```
AIchatbot-project-feature-full-project/
│
├── Backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── routes/          # API endpoints (auth, chat, chatbot, RAG)
│   │   │   └── router.py        # Main router
│   │   ├── core/                # Configuration
│   │   ├── db/                  # Database models and connection
│   │   ├── services/            # RAG services (AI, embeddings, vector store)
│   │   ├── utils/               # PDF/URL extractors, text cleaners
│   │   └── main.py              # FastAPI application
│   ├── data_source/             # PDF documents for knowledge base
│   ├── chroma_db/               # Vector database storage
│   ├── requirements.txt
│   ├── .env
│   └── run_server.py
│
└── Frontend/
    └── travel-chatbot/
        ├── src/
        │   ├── components/      # React components (Home, Login, Register)
        │   └── assets/          # Images
        ├── package.json
        └── package-lock.json
```

---

## Features Implemented

### ✅ Complete RAG Pipeline
1. **Knowledge Ingestion**: PDF and URL content extraction
2. **Text Cleaning**: Removes noise, normalizes formatting
3. **Content Chunking**: Smart chunking with overlap and metadata
4. **Vector Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
5. **Vector Storage**: ChromaDB with semantic search
6. **Context Injection**: Retrieves relevant chunks for LLM
7. **LLM Generation**: Groq (llama-3.1-8b-instant) for responses

### ✅ Authentication System
- User registration and login
- JWT token-based authentication
- MongoDB user storage

### ✅ Chat Interface
- Real-time chat with AI assistant
- Message formatting (lists, bold text, line breaks)
- Theme toggle (dark/light mode)
- Chat history panel
- Auto-scroll and full history access

### ✅ Smart Response Handling
- Greeting detection
- Thank you responses
- Out-of-scope query handling
- Focused, relevant answers

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB running on localhost:27017

### Backend Setup

```bash
cd Backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit .env file with your GROQ_API_KEY and MONGO_URI

# Ingest documents into vector database
python -m app.services.ingestion_engine

# Start server
python run_server.py
```

Server runs at: `http://localhost:8000`

### Frontend Setup

```bash
cd Frontend/travel-chatbot

# Install dependencies
npm install

# Start development server
npm start
```

Application opens at: `http://localhost:3000`

---

## API Endpoints

### Authentication (No prefix)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Chat (No prefix)
- `POST /chat` - Send message to AI (no auth required)

### RAG Testing (Prefix: /api/v1)
- `GET /api/v1/rag/health` - Check RAG system status
- `POST /api/v1/rag/test` - Test RAG with custom query

### Chatbot (Prefix: /api/v1, Auth required)
- `POST /api/v1/chatbot/message` - Send message in conversation

---

## RAG Pipeline Details

### 1. Document Ingestion
- Extracts text from PDFs in `data_source/` folder
- Preserves metadata (source, file type, ingestion date)

### 2. Text Cleaning
- Removes extra whitespace and special characters
- Normalizes unicode and line endings
- Filters page numbers and noise

### 3. Content Chunking
- Chunk size: 500 characters
- Overlap: 100 characters
- Unique chunk IDs (UUID)
- Metadata: source, file_type, chunk_number, timestamp

### 4. Vector Embeddings
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Batch processing for efficiency
- Embedding failure logging

### 5. Vector Storage (ChromaDB)
- Persistent storage in `chroma_db/`
- Cosine similarity search
- Stores: embeddings + metadata + text

### 6. Semantic Retrieval
- Top-K relevant chunks (default: 3)
- Similarity scoring
- Source attribution

### 7. LLM Generation
- Model: Groq `llama-3.1-8b-instant`
- Temperature: 0.5
- Max tokens: 350
- Structured RAG prompts

---

## Configuration

### Environment Variables (.env)
```
MONGO_URI=mongodb://localhost:27017/chat_db
GROQ_API_KEY=your_groq_api_key_here
```

### LLM Settings (ai_services.py)
- Model: `llama-3.1-8b-instant`
- Temperature: 0.5 (balanced)
- Max tokens: 350
- Top-K chunks: 3

---

## Usage Examples

### Simple Chat
```bash
POST http://localhost:8000/chat
{
  "message": "What are the baggage rules for Air India?"
}
```

### RAG Test
```bash
POST http://localhost:8000/api/v1/rag/test
{
  "question": "Tell me about flight delays",
  "top_k": 3
}
```

---

## Project Status

| Feature | Status |
|---------|--------|
| Knowledge Ingestion | ✅ Complete |
| Text Extraction & Cleaning | ✅ Complete |
| Content Chunking | ✅ Complete |
| Metadata Management | ✅ Complete |
| Vector Embeddings | ✅ Complete |
| Vector Database | ✅ Complete |
| Semantic Search | ✅ Complete |
| Context Injection | ✅ Complete |
| LLM Integration | ✅ Complete |
| Authentication | ✅ Complete |
| Chat UI | ✅ Complete |
| Theme Toggle | ✅ Complete |
| Message Formatting | ✅ Complete |

---

## Technologies Used

### Backend
- **FastAPI**: Modern web framework
- **MongoDB**: User and conversation storage
- **ChromaDB**: Vector database
- **LangChain**: LLM integration
- **Groq**: Fast LLM inference
- **Sentence Transformers**: Embeddings
- **PyPDF**: PDF text extraction

### Frontend
- **React**: UI framework
- **CSS3**: Styling with themes
- **Fetch API**: HTTP requests

---


## Future Enhancements

- [ ] Conversation history persistence
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Advanced filtering options
- [ ] Analytics dashboard

---
