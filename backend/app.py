# backend/app.py

from flask import Flask, render_template
from flask_login import LoginManager
from config import get_database
from flask import Blueprint

# Import blueprints and their init functions
from routes.auth_routes import auth, init_auth_routes
from routes.member_routes import member, init_member_routes
from routes.trainer_routes import trainer, init_trainer_routes
from routes.sessions_routes import session, init_sessions_routes
from routes.admin_routes import admin, init_admin_routes
from routes.search_routes import search, init_search_routes

# Flask-Login manager (can be reused across apps)
login_manager = LoginManager()

# Global db variable, initialized later
db = None

def create_app():
    global db

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "h4rD_c0D1nG_a$3crE7_K3Y_15_b4D_pr4cT1C3"

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
    def load_user(user_id):
        return db.get_user(user_id)

    @app.route("/")
    def index():
        return render_template("index.html")

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(member, url_prefix='/members')
    app.register_blueprint(trainer, url_prefix='/trainers')
    app.register_blueprint(session, url_prefix='/sessions')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(search, url_prefix='/search')

    return app
