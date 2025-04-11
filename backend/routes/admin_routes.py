from flask import Blueprint, render_template
from flask_login import login_required

admin = Blueprint('admin', __name__)
db = None  # Will be initialized via init_admin_routes

def init_admin_routes(database):
    global db
    db = database

@admin.route("/admin/members")
@login_required
def manage_members():
    members = db.get_all_members()
    return render_template("admin/manage_members.html", members=members)

@admin.route("/admin/trainers")
@login_required
def manage_trainers():
    trainers = db.get_all_trainers()
    return render_template("admin/manage_trainers.html", trainers=trainers)
