from flask import Blueprint
from controllers.chat_controller import start_conversation, send_message, get_messages

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/start", methods=["POST"])
def start_route():
    return start_conversation()

@chat_bp.route("/send", methods=["POST"])
def send_route():
    return send_message()

@chat_bp.route("/messages", methods=["GET"])
def messages_route():
    return get_messages()
