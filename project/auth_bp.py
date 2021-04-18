import string, random
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user	
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Project
from . import db, mail

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/forgotpassword')
def forgotpassword():
	return render_template('forgotpassword.html')

@auth.route('/resetpassword')
@login_required
def resetpassword():
	return render_template('resetpassword.html')

@auth.route('/resetpassword', methods=['POST'])
@login_required
def resetpassword_post():
	password = request.form.get('password')
	cpassword = request.form.get('cpassword')

	if password != cpassword:
		flash('Passwords did not match please try again.')
		return redirect(url_for('auth.resetpassword'))

	user = User.query.filter_by(email=current_user.email).first()

	user.password = generate_password_hash(password, method='sha256')
	user.needs_reset = False
	db.session.commit()
	
	return redirect(url_for('main.profile'))



@auth.route('/forgotpassword', methods=['POST'])
def forgotpassword_post():
	email = request.form.get('email')

	user = User.query.filter_by(email=email).first()

	if not user:
		flash('No account exists with that email!')
		return redirect(url_for('auth.forgotpassword'))

	def generate_random_password(length):
		alphabet = string.ascii_uppercase + string.digits
		return ''.join(random.choice(alphabet) for i in range(length))

	temporary_password = generate_random_password(10)
	user.password = generate_password_hash(temporary_password, method='sha256')
	user.needs_reset = True
	db.session.commit()
	msg = Message('Password Reset', sender='dcaatimemanagement@gmail.com', recipients=[user.email])
	msg.body = "Your password has been reset. Your temporary password is " + temporary_password + "."
	mail.send(msg)

	flash('A temporary password has been sent to your email.')
	return redirect((url_for('auth.login')))


@auth.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	name = request.form.get('name')
	password = request.form.get('password')
	cpassword = request.form.get('cpassword')

	user = User.query.filter_by(email=email).first()

	if user:
		flash('A user with that email already exists!')
		return redirect(url_for('auth.signup'))
	if password != cpassword:
		flash('Passwords did not match, please try again.')
		return redirect(url_for('auth.signup'))

	new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), needs_reset=False, is_employee=False)

	db.session.add(new_user)
	db.session.commit()

	return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()

	if not user or not check_password_hash(user.password, password):
		flash("Please check your login details and try again")
		return redirect(url_for('auth.login'))

	login_user(user, remember=remember)

	if user.needs_reset:
		return redirect(url_for('auth.resetpassword'))
	return redirect(url_for('main.index'))