# /app/models/call.py
from app import db
from datetime import datetime
from app.utils.custom_types import MyDateTime

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    call_time = db.Column(MyDateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'call_time': self.call_time.isoformat(),
            'duration': self.duration,
            'type': self.type
        }
