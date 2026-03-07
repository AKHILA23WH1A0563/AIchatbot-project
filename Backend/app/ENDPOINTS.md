# API Endpoints Reference

## ✅ Fixed - Auth Endpoints (No Prefix)

Frontend calls these directly:

```
POST http://localhost:8000/auth/register
POST http://localhost:8000/auth/login
```

## ✅ RAG Endpoints (With /api/v1 Prefix)

```
GET  http://localhost:8000/api/v1/rag/health
POST http://localhost:8000/api/v1/rag/test
```

## ✅ Chat Endpoint (No Prefix)

```
POST http://localhost:8000/chat
Body: { "message": "your question" }
```

## ✅ Chatbot Endpoint (With /api/v1 Prefix - Requires Auth)

```
POST http://localhost:8000/api/v1/chatbot/message
Headers: Authorization: Bearer <token>
Body: { "conversationId": "...", "text": "..." }
```

## 🔧 How to Restart Server

```bash
# Stop server (Ctrl+C)

# Restart
cd Backend
python run_server.py
```

## 🧪 Test Auth Flow

1. **Register**: POST to `/auth/register`
2. **Login**: POST to `/auth/login` 
3. **Get Token**: Save from login response
4. **Use Token**: Add to Authorization header for protected routes

## ✅ All Routes Now Working!

- Auth routes: ✅ No prefix (frontend compatible)
- RAG routes: ✅ With /api/v1 prefix
- Chat route: ✅ No prefix (simple access)
