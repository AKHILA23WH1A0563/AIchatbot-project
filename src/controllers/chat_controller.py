from flask import request, jsonify
from models.conversation import Conversation
from models.message import Message
from mongoengine import DoesNotExist


def start_conversation():
    data = request.get_json()
    participants = data.get("participants")

    if not participants or len(participants) < 2:
        return jsonify({"message": "At least two participants required"}), 400

    conversation = Conversation(participants=participants)
    conversation.save()

    return jsonify({
        "message": "Conversation started",
        "conversationId": str(conversation.id)
    }), 201


def send_message():
    data = request.get_json()

    conversation_id = data.get("conversationId")
    sender = data.get("sender")
    text = data.get("text")

    if not all([conversation_id, sender, text]):
        return jsonify({"message": "Missing fields"}), 400

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except DoesNotExist:
        return jsonify({"message": "Conversation not found"}), 404

    message = Message(
        conversation=conversation,
        sender=sender,
        text=text
    )
    message.save()

    return jsonify({"message": "Message sent"}), 201


def get_messages(conversation_id):
    messages = Message.objects(conversation=conversation_id).order_by("created_at")

    result = []
    for msg in messages:
        result.append({
            "id": str(msg.id),
            "sender": str(msg.sender),
            "text": msg.text,
            "createdAt": msg.created_at
        })

    return jsonify(result), 200
