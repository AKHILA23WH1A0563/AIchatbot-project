from mongoengine import Document, ListField, ReferenceField, DateTimeField, CASCADE
from datetime import datetime
from .user import User

class Conversation(Document):
    participants = ListField(ReferenceField(User, reverse_delete_rule=CASCADE))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "conversation", "ordering": ["-created_at"]}

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
