from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))
	needs_reset = db.Column(db.Boolean)
	
class Employee(db.Model):
	employeeID = db.Column(db.Integer, primary_key=True, unique=True)
	firstName = db.Column(db.String(100))
	lastName = db.Coulmn(db.String(100))
	jobTitle = db.Coulmn(db.String(100))
	payRate = db.Coulmn(db.Double)
	
class Project(db.Model):
	projectID = db.Coulmn(db.Integer, primary_key=True, unique=True)
	projectName = db.Coulmn(db.String(100))
	projectOngoing = db.Coumn(db.Boolean)
	
class TimeLog(db.Model):
	projectID = db.Coulmn(db.Integer, primary_key=True)
	employeeID = db.Coulmn(db.Integer)
	currentTime = db.Coulmn(db.date)
	time = db.Coulmn(db.Integer)
	
