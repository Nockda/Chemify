from app import db


class Task_model(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.Text)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    assign_user_id = db.Column(db.Integer, db.ForeignKey("user_model.user_id"))
    assign_user = db.relationship("User_model", back_populates="assigned_tasks")
