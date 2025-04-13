from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import get_database
from flask import Blueprint
import bcrypt

# Import blueprints and their init functions
from routes.auth_routes import auth, init_auth_routes
from routes.member_routes import member, init_member_routes
from routes.trainer_routes import trainer, init_trainer_routes
from routes.sessions_routes import session, init_sessions_routes
from routes.admin_routes import admin, init_admin_routes
from routes.search_routes import search, init_search_routes

# Flask-Login manager
login_manager = LoginManager()

# Global db variable, initialized later
db = None

def create_app():
    global db

    app = Flask(__name__)
    app.secret_key = "h4rD_c0D1nG_a$3crE7_K3Y_15_b4D_pr4cT1C3"

    # Initialize DB
    try:
        db = get_database()
    except Exception as e:
        print('\n'.join([x for x in e.args if type(x) == str]))
        exit(e.args[0])

    # Inject db into route modules
    init_auth_routes(db)
    init_member_routes(db)
    init_trainer_routes(db)
    init_sessions_routes(db)
    init_admin_routes(db)
    init_search_routes(db)

    # Setup login manager
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.get_user_by_id(id)

    @app.route("/")
    def index():
        print("[DEBUG] current_user:", current_user)
        print("[DEBUG] is_authenticated:", current_user.is_authenticated)
        return render_template("index.html")

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(member, url_prefix='/members')
    app.register_blueprint(trainer, url_prefix='/trainers') # implemented through auth so not needed anymore
    app.register_blueprint(session, url_prefix='/sessions')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(search, url_prefix='/search') # Not implemented yet

    return app
