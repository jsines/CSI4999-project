from flask_login import UserMixin
from . import db

#this creates User table
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))
	needs_reset = db.Column(db.Boolean)

#this creates Employee table
class Employee(db.Model):
	employeeID = db.Column(db.Integer, primary_key=True, unique=True)
	firstName = db.Column(db.String(100))
	lastName = db.Column(db.String(100))
	jobTitle = db.Column(db.String(100))
	payRate = db.Column(db.Float)
	
#this creates Project table
class Project(db.Model):
	projectID = db.Column(db.Integer, primary_key=True, unique=True)
	projectName = db.Column(db.String(100))
	projectOngoing = db.Column(db.Boolean)
	
#this creates TimeLog table 
class TimeLog(db.Model):
	projectID = db.Column(db.Integer, primary_key=True)
	employeeID = db.Column(db.Integer)
	currentTime = db.Column(db.Date)
	time = db.Column(db.Integer)
	
