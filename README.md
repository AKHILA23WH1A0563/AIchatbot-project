# AI Travel Chatbot with RAG 

## Project Overview

A full-stack AI Travel Chatbot with complete RAG (Retrieval-Augmented Generation) implementation. The system uses semantic search with ChromaDB, vector embeddings, and LLM integration to provide accurate travel information from PDF documents.

**Latest Updates:** The system now supports **Contextual Memory** (remembering follow-up questions) and **Full Message Persistence** using MongoDB.

**Tech Stack:**

* **Backend**: FastAPI, MongoDB, ChromaDB, LangChain, Groq LLM
* **Frontend**: React, JavaScript, CSS
* **AI/ML**: Sentence Transformers, Semantic Search, RAG Pipeline, Contextual Query Rewriting

---

## Project Structure

```
AIchatbot-project-feature-full-project/
│
├── Backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── routes/          # API (auth, chat, history, RAG)
│   │   │   └── router.py        # Main router
│   │   ├── core/                # Configuration & Security
│   │   ├── db/                  # MongoDB models (User, ChatHistory)
│   │   ├── services/            # RAG, Memory & Query Rewriting
│   │   ├── utils/               # PDF extractors, Text cleaners
│   │   └──               # FastAPI application
│   ├── data_source/             # PDF knowledge base
│   ├── chroma_db/               # Vector database storage
│   ├── requirements.txt
│   └── .env
│
└── Frontend/
    └── travel-chatbot/
        ├── src/
        │   ├── components/      # React components (Chat, History, Auth)
        │   └── assets/          # UI Assets
        └── package.json

```

---

## Features Implemented

### ✅ Complete RAG Pipeline

1. **Knowledge Ingestion**: PDF and URL content extraction.
2. **Text Cleaning**: Removes noise, normalizes formatting.
3. **Content Chunking**: Smart chunking with overlap and metadata.
4. **Vector Embeddings**: Sentence Transformers (all-MiniLM-L6-v2).
5. **Vector Storage**: ChromaDB with semantic search.
6. **Context Injection**: Retrieves relevant chunks for LLM.
7. **LLM Generation**: Groq (llama-3.1-8b-instant) for responses.

### ✅ Chat Message Persistence (User Story #10)

* **Automatic Saving**: Conversations are saved automatically to the `chat_history` collection in MongoDB.
* **Data Integrity**: Stores `user_id`, `session_id`, `query`, `response` (with sources), and `timestamp`.
* **Reference Tracking**: Users can refer back to previous answers and their specific document sources anytime.

### ✅ Contextual Conversation Memory (User Story #11)

* **Follow-up Support**: Chatbot remembers previous questions in the current session.
* **Window Buffer**: Retrieves the last 5–10 messages to maintain short-term context.
* **Query Rewriting**: Applies AI-driven query rewriting before semantic search to ensure follow-up questions (e.g., "What about Air India?") find the right data.
* **Token Control**: Maintains limit control to ensure fast inference.

### ✅ Authentication & Interface

* **Auth**: User registration/login with JWT token-based authentication.
* **UI**: Real-time chat, dark/light mode toggle, and auto-scrolling history.

---

## API Endpoints

### Authentication

* `POST /auth/register` - User registration
* `POST /auth/login` - User login

### Chat & History

* `POST /api/v1/chatbot/message` - Send message (Handles Memory + RAG + Saving)
* `GET /api/v1/chatbot/history/{user_id}` - Retrieve user's saved conversations

### RAG Testing

* `POST /api/v1/rag/test` - Test RAG with custom query (No history)

---

## RAG Pipeline Details

### 1. Document Ingestion & Chunking

* Extracts text from PDFs and creates 500-character chunks with 100-character overlap to preserve context across splits.

### 2. Semantic Retrieval

* Top-K relevant chunks (default: 3) retrieved via Cosine Similarity.

### 3. Contextual Query Rewriter (New)

* If a conversation is ongoing, the LLM reformulates the user's input into a "standalone question" based on chat history before searching ChromaDB.

### 4. Persistence Logic (New)

* Every interaction triggers a background save to MongoDB, ensuring no data loss even if the browser is refreshed.

---

## Project Status

| Feature | Status |
| --- | --- |
| Knowledge Ingestion | ✅ Complete |
| Vector Database | ✅ Complete |
| LLM Integration | ✅ Complete |
| Authentication | ✅ Complete |
| **Chat Message Persistence** | ✅ **Implemented** |
| **Contextual Short-term Memory** | ✅ **Implemented** |
| Theme Toggle & Formatting | ✅ Complete |

---

## Technologies Used

* **Backend**: FastAPI, MongoDB, ChromaDB, LangChain, Groq
* **AI**: Sentence Transformers, Llama 3.1
* **Frontend**: React, CSS3

---

## Future Enhancements

* [ ] Multi-language support
* [ ] Voice input/output
* [ ] Advanced filtering options
* [ ] Analytics dashboard

---

Would you like me to provide the **Python code for the Query Rewriter** or the **MongoDB Schema** used for the persistence logic?