# AI Chatbot Project (Travel Chatbot with RAG-Ready Architecture)

## 📌 Project Overview

This is a **full-stack AI Chatbot application** designed for travel assistance with a clean separation of **backend** and **frontend**. The backend is built using **FastAPI** with a modular architecture, and the frontend is built using **React**. The system supports PDF document processing and is designed to be extended into a **Retrieval-Augmented Generation (RAG)** pipeline for intelligent document-based responses.

---

## 🏗️ Project Structure

```
AIchatbot-project-main/
│
├── Backend/
│   ├── app/
│   │   ├── api/           # API routes (v1 versioning)
│   │   │   ├── deps.py    # Dependency injection
│   │   │   └── v1/
│   │   │       ├── router.py
│   │   │       └── routes/
│   │   │           ├── auth.py      # Authentication endpoints
│   │   │           ├── chat.py      # Chat endpoints
│   │   │           ├── chatbot.py   # Chatbot logic
│   │   │           ├── pdfs.py      # PDF handling
│   │   │           └── travel.py    # Travel-specific endpoints
│   │   ├── core/
│   │   │   └── config.py  # Configuration
│   │   ├── db/
│   │   │   ├── database.py  # Database connection
│   │   │   └── models.py    # Database models
│   │   ├── services/
│   │   │   ├── ai_services.py   # AI integration
│   │   │   └── pdf_service.py   # PDF processing
│   │   ├── utils/
│   │   │   ├── helpers.py      # Utility functions
│   │   │   └── jwt_helper.py   # JWT authentication
│   │   ├── main.py        # Application entry point
│   │   └── __init__.py
│   ├── data_source/       # Data storage
│   ├── run_server.py      # Server launcher
│   ├── requirements.txt   # Backend dependencies
│   └── README.md
│
├── Frontend/
│   └── travel-chatbot/
│       ├── public/        # Static assets
│       ├── src/
│       │   ├── components/
│       │   │   ├── Home.js
│       │   │   ├── Login.js
│       │   │   └── Register.js
│       │   ├── App.js
│       │   └── index.js
│       ├── package.json
│       └── README.md
│
├── requirements.txt       # Root dependencies
└── README.md
```

---

## 🔧 Backend Details

### Technology Stack

* **FastAPI** – Modern Python web framework
* **SQLAlchemy / SQLModel** – ORM for database operations
* **Pydantic** – Data validation
* **PyJWT** – JWT-based authentication
* **python-dotenv** – Environment variable management
* **PyPDF2 / pdfplumber** – PDF processing

### Backend Features

* **Authentication**: JWT-based user authentication with login/register
* **Chat API**: RESTful endpoints for chat interactions
* **PDF Processing**: Upload and parse PDF documents
* **Travel Services**: Travel-specific chatbot functionality
* **Modular Architecture**: Clean separation of concerns (routes, services, models)

### Backend Architecture

The backend follows a **clean modular architecture**:

* **Models**: Database schemas and ORM definitions
* **Services**: Business logic (AI services, PDF processing)
* **Routes**: API endpoints with version control (v1)
* **Utils**: Helper functions and authentication utilities
* **Core**: Configuration management
* **API/Deps**: Dependency injection

---

## ▶️ Running the Backend

### Prerequisites
* Python 3.8+
* pip

### Setup Instructions

From the Backend directory:

```bash
cd Backend
pip install -r requirements.txt
python run_server.py
```

Or from the project root:

```bash
cd Backend
python -m app.main
```

Expected output:

```
Uvicorn running on http://0.0.0.0:8000
API docs available at http://0.0.0.0:8000/docs
```

### API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🎨 Frontend Details

### Technology Stack

* **React 18** – UI framework
* **React Router v6** – Navigation and routing
* **JavaScript / HTML / CSS** – Core web technologies
* **Axios / Fetch API** – HTTP requests to backend
* **Testing Library** – Component testing

### Frontend Features

* **User Authentication**: Login and registration
* **Home Dashboard**: Main chatbot interface
* **Chat Interface**: Real-time chat with the AI chatbot
* **PDF Upload**: Upload and process documents
* **Travel Information**: Travel-specific features
* **Responsive Design**: Mobile-friendly UI

---

## ▶️ Running the Frontend

### Prerequisites
* Node.js 14+ 
* npm

### Setup Instructions

Open a new terminal and navigate to the frontend directory:

```bash
cd Frontend/travel-chatbot
npm install
npm start
```

The application will start at:

```
http://localhost:3000
```

### Available Scripts

* `npm start` – Runs the app in development mode
* `npm build` – Builds the app for production
* `npm test` – Launches the test runner

---

## 📋 Dependencies

### Backend Dependencies

```
FastAPI==0.104.1
uvicorn==0.24.0
SQLAlchemy==2.0.23
pydantic==2.5.0
PyJWT==2.8.1
python-dotenv==1.0.0
bcrypt==4.1.0
PyPDF2==3.17.0
```

### Frontend Dependencies

See [Frontend/travel-chatbot/package.json](Frontend/travel-chatbot/package.json) for complete list:
* React 18.2.0
* React Router DOM 6.22.3
* React Scripts 5.0.1
* Testing Library React 13.4.0

---

## 🚀 Complete Setup & Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AIchatbot-project-main
```

### Step 2: Backend Setup
```bash
cd Backend
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```bash
cd ../Frontend/travel-chatbot
npm install
```

### Step 4: Running the Application

**Terminal 1 - Backend:**
```bash
cd Backend
python run_server.py
```

**Terminal 2 - Frontend:**
```bash
cd Frontend/travel-chatbot
npm start
```

The application will be accessible at `http://localhost:3000`

---

## 🔐 Environment Variables

Create a `.env` file in the `Backend/` directory with the following variables:

```
DATABASE_URL=<your-database-url>
JWT_SECRET_KEY=<your-secret-key>
CORS_ORIGINS=http://localhost:3000
DEBUG=True
AI_API_KEY=<your-ai-api-key>
```

---

## 📝 API Endpoints

### Authentication
- `POST /api/v1/auth/register` – Register new user
- `POST /api/v1/auth/login` – User login
- `GET /api/v1/auth/me` – Get current user (requires auth)

### Chat
- `POST /api/v1/chat/send` – Send chat message
- `GET /api/v1/chat/history` – Get chat history
- `GET /api/v1/chat/{message_id}` – Get specific message

### PDF Processing
- `POST /api/v1/pdfs/upload` – Upload PDF document
- `GET /api/v1/pdfs/list` – List uploaded PDFs
- `DELETE /api/v1/pdfs/{pdf_id}` – Delete PDF

### Travel
- `GET /api/v1/travel/destinations` – Get travel destinations
- `POST /api/v1/travel/recommendations` – Get travel recommendations

---

## 🤖 Future Enhancements (RAG Pipeline)

The architecture is designed to support:
* Vector embeddings for document processing
* Semantic search over uploaded PDFs
* Context-aware responses using retrieved documents
* Multi-modal input (text, images, documents)
* LLM integration for intelligent responses

---

## 📘 Important Notes

* Ensure all environment variables are configured in `.env` before running the backend
* The FastAPI server must be running for the frontend to function
* API documentation is automatically generated and available at `http://localhost:8000/docs`
* Frontend development server uses port 3000 (configurable in `.env`)

---

## ✅ Status

✔ Backend & Frontend properly separated
✔ Modular, scalable architecture with versioned APIs
✔ Authentication and authorization implemented
✔ PDF processing capabilities added
✔ Travel-specific features integrated
✔ Ready for RAG pipeline extension

---
