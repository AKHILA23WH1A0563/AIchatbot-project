from mongoengine import Document, ReferenceField, StringField, DateTimeField, CASCADE
from datetime import datetime
from .user import User
from .conversation import Conversation

class Message(Document):
    conversation = ReferenceField(Conversation, reverse_delete_rule=CASCADE)
    sender = ReferenceField(User, reverse_delete_rule=CASCADE)
    text = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "message", "ordering": ["-created_at"]}

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
