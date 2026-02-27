# AI Chatbot Project (RAG-Ready Architecture)

## Project Overview

This project is a full-stack AI Chatbot application with a clean separation of backend and frontend. The backend is built using Flask with a modular MVC-style architecture, and the frontend is built using React.

The system includes authentication, chat handling, and a structured RAG preprocessing pipeline implemented up to the content chunking stage.

---

## Project Structure

```
AIchatbot-project-main/
│
├── backend/
│   ├── src/
│   │   ├── config/          # Database configuration
│   │   ├── controllers/     # Business logic (auth, chat)
│   │   ├── middleware/      # Authentication & request middleware
│   │   ├── models/          # MongoDB models (schemas)
│   │   ├── routes/          # API route definitions (Blueprints)
│   │   ├── services/        # RAG processing (extraction, cleaning, chunking)
│   │   ├── __init__.py
│   │   └── app.py           # Flask application entry point
│   ├── requirements.txt     # Backend dependencies
│   └── .env                 # Environment variables
│
├── frontend/
│   └── travel-chatbot/
│       ├── public/
│       ├── src/
│       ├── package.json
│       └── package-lock.json
│
├── architecture_diagram.png
└── README.md
```

---

## Backend Details

### Technology Stack

- Flask
- MongoEngine
- Flask-CORS
- PyJWT
- Python-dotenv
- PyPDF2

### Backend Architecture

The backend follows a modular architecture:

- Models: MongoDB schemas
- Controllers: Business logic
- Routes: API endpoints using Flask Blueprints
- Middleware: Authentication and request validation
- Services: RAG preprocessing logic

---

## Running the Backend

From the project root:

```bat
cd backend
pip install -r requirements.txt
python -m src.app
```

Expected output:

```
Running on http://0.0.0.0:5000
```

---

## Frontend Details

### Technology Stack

- React
- JavaScript / HTML / CSS
- Axios / Fetch API

---

## Running the Frontend

Open a new terminal:

```bat
cd frontend\travel-chatbot
npm install
npm start
```

The application will start at:

```
http://localhost:3000
```

---

## Authentication APIs

| Method | Endpoint        | Description        |
|--------|----------------|--------------------|
| POST   | /auth/register | User registration  |
| POST   | /auth/login    | User login         |

---

## RAG Preprocessing Pipeline (Implemented)

The project includes a RAG preprocessing module implemented up to content chunking.

### Workflow

Data Source → Text Extraction → Text Cleaning → Chunking

---

## Step 1: Text Extraction

- Extracts page-wise text from PDF files
- Extracts full content from text files
- Preserves page number metadata

---

## Step 2: Text Cleaning


- Removes extra whitespace
- Normalizes formatting
- Removes unwanted special characters
- Maintains structured content

---

## Step 3: Content Chunking

Extracted text is divided into smaller segments for efficient processing.

### Chunking Strategy

- Fixed chunk size (e.g., 500 characters)
- Overlapping chunks (e.g., 100 characters overlap)
- Unique chunk IDs generated
- Source file name retained
- Page number metadata retained

### Sample Chunk Structure

```json
{
  "chunk_id": "document_chunk_01",
  "content": "Sample chunk text...",
  "source": "file_name.pdf",
  "page_number": 2
}
```

---

## Status

Backend and frontend integrated  
Authentication implemented  
Document extraction completed  
Text cleaning completed  
Content chunking with metadata completed  
