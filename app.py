import os

from flask import Flask
from flask_login import (
	LoginManager,
	current_user,
	login_required,
	login_user,
	logout_user,
)

# Flask Setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Session Management
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

@app.route("/")
def hello():
	return "Hello world!"

#@app.route("/login", methods=['GET', 'POST'])
#def login():


if __name__ == "__main__":
	app.run()