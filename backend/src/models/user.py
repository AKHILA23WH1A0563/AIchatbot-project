from mongoengine import Document, StringField, DateTimeField, signals
from datetime import datetime
import bcrypt

class User(Document):
    full_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    mobile_number = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "user", "ordering": ["-created_at"]}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if "password" in getattr(document, "_changed_fields", []):
            salt = bcrypt.gensalt()
            document.password = bcrypt.hashpw(document.password.encode(), salt).decode()
            document.updated_at = datetime.utcnow()

    def match_password(self, entered_password):
        return bcrypt.checkpw(entered_password.encode(), self.password.encode())

signals.pre_save.connect(User.pre_save, sender=User)
