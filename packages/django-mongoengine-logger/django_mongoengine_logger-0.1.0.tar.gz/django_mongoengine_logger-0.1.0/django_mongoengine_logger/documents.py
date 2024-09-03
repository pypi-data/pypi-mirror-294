from mongoengine import DateTimeField, Document, DynamicField, IntField, StringField


class LogDocument(Document):
    meta = {
        "collection": "django_logs",
        "indexes": [
            "level",
            "timestamp",
            "message",
            "module",
            "line",
            "func",
        ],
    }

    level = StringField(required=True)
    timestamp = DateTimeField(required=True)
    message = DynamicField(required=True)
    module = StringField(required=True)
    line = IntField(required=True)
    func = StringField()
