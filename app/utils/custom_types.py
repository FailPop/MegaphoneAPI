# /app/utils/custom_types.py
from sqlalchemy.types import TypeDecorator, DateTime
from datetime import datetime

class MyDateTime(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    def process_result_value(self, value, dialect):
        return value
