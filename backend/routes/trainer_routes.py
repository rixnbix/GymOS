from flask import Blueprint, render_template

trainer = Blueprint('trainer', __name__)
db = None  # Will be set in init_trainer_routes

def init_trainer_routes(database):
    global db
    db = database

@trainer.route("/trainers/<int:trainer_id>")
def trainer_profile(trainer_id):
    trainer_data = db.get_trainer(trainer_id)
    return render_template("trainer_profile.html", trainer=trainer_data)

@trainer.route("/trainers")
def trainer_list():
    trainers = db.get_all_trainers()
    return render_template("trainer_list.html", trainers=trainers)
