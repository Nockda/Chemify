from app import db
from datetime import datetime
from typing import Optional


class Task_history_model(db.Model):
    task_history_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id: int = db.Column(db.Integer, nullable=False)
    task_name: Optional[str] = db.Column(db.Text)
    description: Optional[str] = db.Column(db.Text)
    status: str = db.Column(db.String(20), nullable=False)
    action_type: str = db.Column(db.String(0), nullable=False)
    transaction_time: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_user: Optional[str] = db.Column(db.String(255))
