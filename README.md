# AI Travel Chatbot with RAG

## Project Overview

A full-stack AI Travel Chatbot with complete RAG (Retrieval-Augmented Generation) implementation. The system uses semantic search with ChromaDB, vector embeddings, and LLM integration to provide accurate travel information from PDF documents.

The system supports contextual memory for follow-up questions and full message persistence using MongoDB, enabling users to maintain conversation context and access their chat history across sessions.

## Tech Stack

* **Backend**: FastAPI, MongoDB, ChromaDB, LangChain, Groq LLM
* **Frontend**: React, JavaScript, CSS
* **AI/ML**: Sentence Transformers, Semantic Search, RAG Pipeline, Contextual Query Rewriting

## Project Structure

```
AIchatbot-project-main/
│
├── Backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── routes/          # API endpoints (auth, chat, sessions)
│   │   │   └── router.py        # Main router
│   │   ├── core/                # Configuration & Security
│   │   ├── db/                  # MongoDB models (User, ChatHistory)
│   │   ├── services/            # RAG, Memory & Query Rewriting
│   │   ├── utils/               # PDF extractors, Text cleaners
│   │   └── main.py              # FastAPI application
│   ├── data_source/             # PDF knowledge base
│   ├── chroma_db/               # Vector database storage
│   ├── requirements.txt
│   └── .env
│
└── Frontend/
    └── travel-chatbot/
        ├── src/
        │   ├── components/      # React components (Chat, History, Auth)
        │   └── assets/          # UI Assets
        └── package.json
```

## Key Features

### Complete RAG Pipeline

1. **Knowledge Ingestion**: PDF content extraction and processing
2. **Text Cleaning**: Noise removal and formatting normalization
3. **Content Chunking**: Smart chunking with overlap and metadata
4. **Vector Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
5. **Vector Storage**: ChromaDB with semantic search capabilities
6. **Context Injection**: Retrieves relevant chunks for LLM processing
7. **LLM Generation**: Groq (llama-3.1-8b-instant) for response generation

### Chat Memory & Persistence

* **Automatic Saving**: Conversations saved to MongoDB with complete metadata
* **Data Integrity**: Stores user_id, session_id, query, response, sources, and timestamp
* **Reference Tracking**: Users can access previous answers and document sources
* **Follow-up Support**: Contextual memory for natural conversation flow
* **Query Rewriting**: AI-driven query enhancement for better search results

### Session Management

* **Session Navigation**: Browse and load previous chat sessions
* **Session Deletion**: Remove unwanted conversations with confirmation
* **Auto Restore**: Automatically loads the most recent session on login
* **Real-time Updates**: Session list updates automatically after operations

### Authentication & Interface

* **JWT Authentication**: Secure user registration and login
* **Responsive UI**: Real-time chat interface with dark/light mode toggle
* **Auto-scrolling**: Smooth message display and navigation

## RAG Pipeline Details

### Document Processing
* Extracts text from PDF documents in the data_source directory
* Creates 500-character chunks with 100-character overlap for context preservation
* Generates vector embeddings using Sentence Transformers

### Semantic Retrieval
* Retrieves top-K relevant chunks (default: 3) using cosine similarity
* Applies MMR (Maximal Marginal Relevance) for diverse results
* Filters chunks based on query topic relevance

### Contextual Processing
* Rewrites follow-up questions into standalone queries using chat history
* Maintains conversation context with configurable message window
* Optimizes token usage for efficient LLM processing

## API Endpoints

### Authentication
* `POST /auth/register` - User registration
* `POST /auth/login` - User login

### Chat Operations
* `POST /api/v1/chatbot/message` - Send message with RAG processing
* `GET /api/v1/chatbot/history/{user_id}` - Retrieve user chat history

### Session Management
* `GET /api/v1/chatbot/session/{session_id}` - Load specific session
* `DELETE /api/v1/chatbot/session/{session_id}` - Delete session
* `GET /api/v1/chatbot/last-session/{user_id}` - Get most recent session

### Testing
* `POST /api/v1/rag/test` - Test RAG functionality

## Frontend Features

* **Real-time Chat**: Instant message exchange with typing indicators
* **Session Sidebar**: Easy navigation between chat sessions
* **Theme Toggle**: Dark/light mode support
* **Responsive Design**: Works across desktop and mobile devices
* **Message History**: Persistent chat history with source references
* **Custom Modals**: Professional confirmation dialogs for user actions

## Future Enhancements

* [ ] Multi-language support for international users
* [ ] Advanced filtering and search options
* [ ] Analytics dashboard for usage insights
* [ ] Integration with external travel APIs
* [ ] Mobile application development