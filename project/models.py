from flask_login import UserMixin
from . import db

#this creates User table
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))
	needs_reset = db.Column(db.Boolean)
	is_employee = db.Column(db.Boolean)

#this creates Employee table
class Employee(db.Model):
	employeeID = db.Column(db.Integer, primary_key=True, unique=True)
	company_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer, unique=True)
	name = db.Column(db.String(1000))
	emp_email = db.Column(db.String(100), unique=True)
	jobTitle = db.Column(db.String(100))
	payRate = db.Column(db.Float)
	
#this creates Project table
class Project(db.Model):
	projectID = db.Column(db.Integer, primary_key=True, unique=True)
	companyID = db.Column(db.Integer)
	projectName = db.Column(db.String(100))
	projectOngoing = db.Column(db.Boolean)
	
#this creates TimeLog table 
class TimeLog(db.Model):
	projectID = db.Column(db.Integer, primary_key=True)
	employeeID = db.Column(db.Integer)
	currentTime = db.Column(db.Date)
	time = db.Column(db.Integer)
	
class ExpenseLog(db.Model):
	expenseLogID = db.Column(db.Integer, primary_key=True)
	projectID = db.Column(db.Integer)
	employeeID = db.Column(db.Integer)
	expenseName = db.Column(db.String(1000))
	expenseAmount = db.Column(db.Numeric(13,2))
	expenseDescription = db.Column(db.String(10000))