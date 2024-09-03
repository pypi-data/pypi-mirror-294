import json
import logging
from datetime import datetime

from django.utils.module_loading import import_string
from mongoengine import Document


def is_json_loadable(message):
    try:
        json.loads(message)
        return True
    except json.JSONDecodeError:
        return False


class MongoDBHandler(logging.Handler):
    """
    A logging handler that writes log messages to a MongoDB collection using MongoEngine.

    Attributes:
        log_document (Document): The MongoEngine document class used to store log entries.
    """

    def __init__(
        self, log_document_path="django_mongoengine_logger.documents.LogDocument"
    ):
        """
        Initialize the MongoDBHandler.

        Args:
            log_document_path (str): The import path to the MongoEngine document class.
        """
        super().__init__()
        self.log_document: Document = import_string(log_document_path)

        # check if the log document is MongoEngine Document
        if not issubclass(self.log_document, Document):
            raise ValueError(
                "log_document_path must be a subclass of mongoengine.Document"
            )

        # check if the log document has the required fields
        required_fields = ["level", "timestamp", "message", "module", "line", "func"]
        if not all(field in self.log_document._fields for field in required_fields):
            raise ValueError(
                f"log_document must have the following fields: {', '.join(required_fields)}"
            )

    def emit(self, record):
        """
        Emit a log record.

        Args:
            record (logging.LogRecord): The log record to be logged.
        """
        try:
            log_entry = self.format(record)
            self.log_document(
                level=log_entry["level"],
                timestamp=log_entry["created"],
                message=log_entry["message"],
                module=log_entry["pathname"],
                line=log_entry["lineno"],
                func=log_entry["funcName"],
            ).save()
        except Exception as e:
            self.handleError(record)

    def format(self, record):
        """
        Format the log record into a dictionary.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            dict: The formatted log record.
        """
        try:
            message = json.loads(record.getMessage())
        except json.JSONDecodeError:
            message = record.getMessage()

        return {
            "level": record.levelname,
            "message": message,
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "created": datetime.fromtimestamp(record.created),
            "msecs": record.msecs,
            "relativeCreated": record.relativeCreated,
            "thread": record.thread,
            "threadName": record.threadName,
            "process": record.process,
            "processName": record.processName,
        }
