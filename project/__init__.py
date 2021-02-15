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
from flask_mail import Mail, Message

db = SQLAlchemy()
mail = Mail()
def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.urandom(24)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
	db.init_app(app)

	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'dcaatimemamangement@gmail.com'
	app.config['MAIL_PASSWORD'] = os.environ.get('MAILPWD')
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail.init_app(app)

	# Login/Session management
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	from .models import User

	@login_manager.user_loader
	def load_user(user_id):
			return User.query.get(int(user_id))

	# Loading in routing blueprints
	from .auth_bp import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)
	from .main_bp import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app