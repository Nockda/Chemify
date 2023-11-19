from flask import abort, app, jsonify, request
from sqlalchemy.event import listens_for
from sqlalchemy.orm.exc import NoResultFound

# from app.models import db
from app import app, db
from model.task_model import Task_model
from model.user_model import User_model
from model.task_history_model import Task_history_model


@app.route("/tasks/<int:user_no>", methods=["GET", "POST"])
def tasks(user_no):
    if request.method == "GET":
        if user_no:
            user_tasks = Task_model.query.filter(
                Task_model.assign_user.has(User_model.user_no == user_no)
            ).all()
            tasks_list = [
                {
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "description": task.description,
                    "status": task.status,
                    "assign_user": task.assign_user,
                }
                for task in user_tasks
            ]
            return jsonify({"tasks": tasks_list})

    elif request.method == "POST":
        data = request.json
        statusValidationCheck(data)
        user = User_model.query.filter_by(user_no=user_no).first()
        new_task = Task_model(
            task_name=data["task_name"],
            description=data["description"],
            status=data["status"],
            assign_user=user,
        )
        db.session.add(new_task)
        # new_task has no task_id. so query db and search the data to register the history table.
        registered_task = Task_model.query.filter_by(
            task_name=data["task_name"]
        ).first()
        add_task_to_history(registered_task, user_no, "Creat")
        db.session.commit()
        return jsonify({"message": "Task added successfully!"})


@app.route("/tasks/update/<int:user_no>", methods=["PUT"])
def update_task(user_no):
    data = request.json
    statusValidationCheck(data)

    task_id = data.get("task_id")

    try:
        user = User_model.query.filter_by(user_no=user_no).one()
        task = Task_model.query.filter_by(task_id=task_id, assign_user=user).one()

        # Update task properties
        task.task_name = data["task_name"]
        task.description = data["description"]
        task.status = data["status"]
        assigned_user = User_model.query.get(data.get("assign_user"))
        task.assign_user = assigned_user
        add_task_to_history(task, user_no, "Update")
        db.session.commit()

        return jsonify({"message": "Task updated successfully!"})
    except NoResultFound:
        return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/delete/<int:user_no>", methods=["DELETE"])
def delete_task(user_no):
    data = request.json
    task_id = data.get("task_id")

    try:
        user = User_model.query.filter_by(user_no=user_no).one()
        task = Task_model.query.filter_by(task_id=task_id, assign_user=user).one()

        db.session.delete(task)
        add_task_to_history(task, user_no, "Delete")
        db.session.commit()

        return jsonify({"message": "Task deleted successfully!"})
    except NoResultFound:
        return jsonify({"error": "Task not found"}), 404


def statusValidationCheck(data):
    status_combo = ["Pending", "Doing", "Blocked", "Done"]
    if data["status"] not in status_combo:
        abort(400, description="You input the wrong status value")


##################################################################
################### History table event listener##################
##################################################################


def add_task_to_history(task, user_no, action_type):
    task_info = {
        "task_id": task.task_id,
        "task_name": task.task_name,
        "description": task.description,
        "status": task.status,
        "transaction_user": user_no,
        "action_type": action_type,
    }

    task_history = Task_history_model(**task_info)

    db.session.add(task_history)
    db.session.commit()
