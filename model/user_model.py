from app import app, db
from model.task_model import Task_model


class User_model(db.Model):
    user_no: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: str = db.Column(db.Text, nullable=False, unique=True)
    user_name: str = db.Column(db.Text, nullable=False)

    assigned_tasks = db.relationship("Task_model", back_populates="assign_user")
