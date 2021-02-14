import string, random
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from .models import User, Employee
from . import db, mail

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)

@main.route('/invite')
@login_required
def invite():
	return render_template('invite.html')

@main.route('/invite', methods=['POST'])
@login_required
def invite_post():
	# Find data from form
	email = request.form.get('email')
	name = request.form.get('name')

	# Check if user exists already
	user = User.query.filter_by(email=email).first()
	if user:
		flash('A user with that email already exists!')
		return redirect(url_for('main.invite'))

	# Generate temporary password
	def generate_random_password(length):
		alphabet = string.ascii_uppercase + string.digits
		return ''.join(random.choice(alphabet) for i in range(length))
	temporary_password = generate_random_password(10)

	# Add user,employee to database
	new_user = User(email=email, name=name, password=generate_password_hash(temporary_password, method='sha256'), needs_reset=True, is_employee=True)
	db.session.add(new_user)
	db.session.commit()
	user_entry = User.query.filter_by(email=email).first()
	new_employee = Employee(user_id=user_entry.id, name=name, jobTitle='Fake Title', payRate=9.00)
	db.session.add(new_employee)
	db.session.commit()
	

	# Email user that their account has been created
	msg = Message('Account Created', sender='dcaatimemamangement@gmail.com', recipients=[email])
	msg.body = "An account has been created for you. Your temporary password is " + temporary_password + "."
	mail.send(msg)

	return redirect(url_for('main.profile'))