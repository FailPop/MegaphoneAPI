# /app/models/phone.py
from app import db


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'model': self.model,
            'owner': self.owner
        }
