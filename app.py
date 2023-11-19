from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def root():
    return "this is the api of managing task"


from controllers import *
from model.user_model import User_model
from model.task_model import Task_model
from model.task_history_model import Task_history_model

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
