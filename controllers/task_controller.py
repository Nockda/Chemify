from flask import app, jsonify, request

# from app.models import db
from app import app, db
from model.task_model import Task_model


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        all_tasks = Task_model.query.all()
        tasks_list = [
            {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "description": task.description,
                "status": task.status,
                "assign_user": task.assign_user,
            }
            for task in all_tasks
        ]
        return jsonify({"tasks": tasks_list})
    elif request.method == "POST":
        data = request.json
        status_combo = ["Pending", "Doing", "Blocked", "Done"]
        if data["status"] not in status_combo:
            return jsonify({"error": "You input the wrong status value"}), 400
        new_task = Task_model(
            task_name=data["task_name"],
            description=data["description"],
            status=data["status"],
            assign_user=data.get("assign_user"),
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task added successfully!"})
