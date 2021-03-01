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
	projectName = db.Column(db.String(100))
	projectOngoing = db.Column(db.Boolean)
	EmployerID = db.Column(db.Integer)
	
#this creates TimeLog table 
class TimeLog(db.Model):
	TimeLogID = db.Column(db.Integer, primary_key=True)
	projectName = db.Column(db.String(100))
	currentTime = db.Column(db.Date)
	time = db.Column(db.Integer)

#this creates the Assignment table (where all project-employee asignments go and can be read)
class Assignments(db.Model):
	AssignmentID = db.Column(db.Integer, primary_key=True) #this is a table identifier; not actually used
	projectName = db.Column(db.String(100))                #this is the name for the selected project
	employeeID = db.Column(db.Integer)                     #this will be entered by the employer; this is the "assigned" employee
	UserID = db.Column(db.Integer)                         #this will be used for visibility checks

	
class ExpenseLog(db.Model):
	expenseLogID = db.Column(db.Integer, primary_key=True)
	projectID = db.Column(db.Integer)
	employeeID = db.Column(db.Integer)
	expenseName = db.Column(db.String(1000))
	expenseAmount = db.Column(db.Numeric(13,2))
	expenseDescription = db.Column(db.String(10000))