from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

session = Blueprint('session', __name__)
db = None  # Will be initialized via init_sessions_routes

def init_sessions_routes(database):
    global db
    db = database

@session.route("/training_sessions")
@login_required
def training_sessions():
    sessions = db.get_training_sessions(current_user.id)
    return render_template("training_sessions.html", sessions=sessions)

@session.route("/training_sessions/new", methods=["GET", "POST"])
@login_required
def new_training_session():
    if request.method == "POST":
        trainer_id = request.form.get("trainer_id")
        session_date = request.form.get("session_date")
        db.create_training_session(current_user.id, trainer_id, session_date)
        return redirect(url_for('session.training_sessions'))
    trainers = db.get_available_trainers()
    return render_template("new_training_session.html", trainers=trainers)
