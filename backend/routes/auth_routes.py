from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)
db = None  # Will be set via init_auth_routes

def init_auth_routes(database):
    global db
    db = database

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = "admin"  # Hardcoded for now, or set based on logic

        print(f"[DEBUG] Signup form received: {email}")

        # Create the user with the received data
        new_user = db.create_user(email, password, role)

        if new_user:
            flash("Account created successfully. Please log in.")
            return redirect(url_for('auth.login'))
        else:
            flash("Username already exists or invalid input.")
    
    return render_template("signup.html")



@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.get_user(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))  # Assuming your home is the index page
        else:
            flash("Invalid username or password.")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
