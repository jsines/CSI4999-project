import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
	LoginManager,
	current_user,
	login_required,
	login_user,
	logout_user,
)

db = SQLAlchemy()
def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.urandom(24)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

	db.init_app(app)

	# Loading in routing blueprints
	from .auth_bp import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)
	from .main_bp import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

# Session Management
#login_manager = LoginManager()
#login_manager.init_app(app)

#if __name__ == "__main__":
#	app.run()