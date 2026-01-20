# src/app.py
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from config.db import connect_db

app = Flask(__name__)
CORS(app)  # allow frontend to access backend

connect_db()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
