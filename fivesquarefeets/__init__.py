import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Flask-Migrate

db = SQLAlchemy()
migrate = Migrate()  # Initialize Migrate instance
login_manager = LoginManager()

def create_app(config_filename=None):
    app = Flask(__name__)

    # Load configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'b6fdd37cb1bbdcdd6417af7df90b1494')
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app context
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate
    login_manager.init_app(app)

    # Set up login manager configurations
    login_manager.login_view = 'main.login'  # Update to reference blueprint
    login_manager.login_message_category = 'info'

    # Register blueprints
    from fivesquarefeets.routes import bp as main_bp  # Import the blueprint
    app.register_blueprint(main_bp)  # Register the main blueprint

    with app.app_context():
        db.create_all()  # Create all tables
    return app
