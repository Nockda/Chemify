from app import db
from typing import Optional


class Task_model(db.Model):
    task_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name: Optional[str] = db.Column(db.Text)
    description: Optional[str] = db.Column(db.Text)
    status: str = db.Column(db.String(20), nullable=False)
    assign_user_id: Optional[int] = db.Column(
        db.Integer, db.ForeignKey("user_model.user_no"), nullable=False
    )
    assign_user = db.relationship("User_model", back_populates="assigned_tasks")
