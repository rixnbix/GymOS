from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

member = Blueprint('member', __name__)
db = None  # Will be initialized from app.py via init_member_routes

def init_member_routes(database):
    global db
    db = database

@member.route("/members/<int:member_id>")
@login_required
def member_profile(member_id):
    if current_user.id != member_id:  # Ensure users can't access others' profiles
        return redirect(url_for('index'))  # Use 'index' instead of 'home' if that's your route
    member_data = db.get_member(member_id)
    return render_template("member_profile.html", member=member_data)
