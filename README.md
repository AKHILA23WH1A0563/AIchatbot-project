# AI Chatbot Project (RAG-Ready Architecture)

## 📌 Project Overview

This project is a **full-stack AI Chatbot application** with a clean separation of **backend** and **frontend**. The backend is built using **Flask** with a modular MVC-style architecture, and the frontend is built using **React**. The system is designed to be extended into a **Retrieval-Augmented Generation (RAG)** pipeline in future phases.

---

## 🏗️ Project Structure

```
AIchatbot-project-main/
│
├── backend/
│   ├── src/
│   │   ├── config/        # Database configuration
│   │   ├── controllers/   # Business logic (auth, chat)
│   │   ├── middleware/    # Authentication & request middleware
│   │   ├── models/        # MongoDB models (schemas)
│   │   ├── routes/        # API route definitions (Blueprints)
│   │   ├── __init__.py
│   │   └── app.py         # Flask application entry point
│   ├── requirements.txt   # Backend dependencies
│   └── .env               # Environment variables
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

## 🔧 Backend Details

### Technology Stack

* **Flask** – Backend framework
* **MongoEngine** – MongoDB ORM
* **Flask-CORS** – Cross-origin support
* **JWT (PyJWT)** – Authentication
* **Python-dotenv** – Environment variable management

### Backend Architecture

The backend follows a **clean modular architecture**:

* **Models**: Database schemas (MongoDB)
* **Controllers**: Business logic
* **Routes**: API endpoints using Flask Blueprints
* **Middleware**: Authentication and request validation

---

## ▶️ Running the Backend

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

## 🎨 Frontend Details

### Technology Stack

* **React**
* **JavaScript / HTML / CSS**
* **Axios / Fetch API** (for backend communication)

---

## ▶️ Running the Frontend

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

## 🔐 Authentication APIs (Sample)

| Method | Endpoint       | Description       |
| ------ | -------------- | ----------------- |
| POST   | /auth/register | User registration |
| POST   | /auth/login    | User login        |

---

## 🧠 Future Scope (RAG Integration)

This project is designed to support **Retrieval-Augmented Generation (RAG)** features such as:

* Document & website ingestion
* Vector embeddings & vector database
* Semantic search
* Context injection into LLMs
* Source-based answer generation

---

## 📘 Notes

* Ensure MongoDB is running before starting the backend
* Environment variables must be configured in `.env`
* Use `python -m src.app` to avoid import issues

---

## ✅ Status

✔ Backend & Frontend separated
✔ Clean modular architecture
✔ Ready for RAG pipeline extension

---
