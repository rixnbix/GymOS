from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

session = Blueprint('session', __name__)
db = None  # Will be initialized via init_sessions_routes

def init_sessions_routes(database):
    global db
    db = database

@session.route("/training_sessions")
@login_required
def training_sessions():
    try:
        # Fetch all sessions
        sessions = db.get_training_sessions()
        eligible_members = db.get_eligible_members()  # Get Premium members
        print(f"[DEBUG] Eligible Members: {eligible_members}")
        # Render the template with the sessions
        return render_template("training_sessions.html", sessions=sessions, eligible_members=eligible_members)
    except Exception as e:
        print(f"[ERROR] Failed to fetch training sessions: {e}")
        return render_template("training_sessions.html", sessions=[], eligible_members=[])


@session.route("/training_sessions/new", methods=["GET", "POST"])
@login_required
def new_training_session():
    if request.method == "POST":
        trainer_id = request.form.get("trainer_id")
        session_date = request.form.get("session_date")
        
        print(f"[DEBUG] trainer_id: {trainer_id}, session_date: {session_date}")  # Debug print

        db.create_class(current_user.id, trainer_id, session_date)
        return redirect(url_for('session.training_sessions'))
    trainers = db.get_all_trainers()
    return render_template("new_training_session.html", trainers=trainers)

@session.route("/sessions/enroll/<session_id>", methods=["POST"])
@login_required
def enroll_member(session_id):
    try:
        # Get the member_id from the form data
        member_id = request.form.get("member_id")
        print(f"[DEBUG] Enrolling member {member_id} in session {session_id}")  # Debugging
        
        # Generate a new EnrollmentID using the sequence (similar to user_id_seq)
        with db.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id_seq.NEXTVAL FROM DUAL")
                enrollment_id = cursor.fetchone()[0]
                
                # Insert into Class_Enrollment table
                cursor.execute("""
                    INSERT INTO Class_Enrollment (EnrollmentID, MemberID, ClassID)
                    VALUES (:1, :2, :3)
                """, [enrollment_id, member_id, session_id])
                conn.commit()

        flash("Member successfully enrolled.", "success")
        return redirect(url_for('session.training_sessions'))
    except Exception as e:
        flash(f"Error enrolling member: {e}", "danger")
        return redirect(url_for('session.training_sessions'))
