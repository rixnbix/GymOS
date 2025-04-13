from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
from datetime import datetime

admin = Blueprint('admin', __name__)
db = None  # Will be initialized via init_admin_routes

def init_admin_routes(database):
    global db
    db = database

@admin.route('/members', methods=['GET', 'POST'])
@login_required
def manage_members():
    members = db.get_all_members()  # Query your database for all members
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        membership_type = request.form['membership_type']
        join_date_str = request.form['join_date']
        
        try:
            join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
            db.add_member(name, contact_info, membership_type, join_date)
        except Exception as e:
            print(f"[ERROR] Failed to add member: {e}")

        return redirect(url_for('admin.manage_members'))

    return render_template('manage_members.html', members=members)


@admin.route('/trainers', methods=['GET', 'POST'])
@login_required
def manage_trainers():
    trainers = db.get_all_trainers()  # Query your database for all trainers
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        
        if not name or not specialization:
            flash('Name and Specialization are required fields!', 'danger')
            return redirect(url_for('admin.manage_trainers'))

        try:
            db.add_trainer(name, specialization)  # Add new trainer to the database
            flash('Trainer added successfully!', 'success')
        except Exception as e:
            print(f"[ERROR] Failed to add trainer: {e}")
            flash('Failed to add trainer. Please try again later.', 'danger')

        return redirect(url_for('admin.manage_trainers'))

    return render_template('manage_trainers.html', trainers=trainers)


# Delete Member Route
@admin.route('/members/<int:member_id>/delete', methods=['POST'])
@login_required
def delete_member(member_id):
    try:
        db.delete_member(member_id)  # Use your DB method to delete the member by their ID
        return redirect(url_for('admin.manage_members'))  # Redirect back to manage members page
    except Exception as e:
        print(f"[ERROR] Failed to delete member: {e}")
        return redirect(url_for('admin.manage_members'))  # Redirect on failure as well

# Delete Trainer Route
@admin.route('/trainers/<int:trainer_id>/delete', methods=['POST'])
@login_required
def delete_trainer(trainer_id):
    try:
        db.delete_trainer(trainer_id)  # Use your DB method to delete the trainer by their ID
        return redirect(url_for('admin.manage_trainers'))  # Redirect back to manage trainers page
    except Exception as e:
        print(f"[ERROR] Failed to delete trainer: {e}")
        return redirect(url_for('admin.manage_trainers'))  # Redirect on failure as well
