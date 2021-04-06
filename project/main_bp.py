import string, random, datetime 
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from .models import User, Employee, Project, TimeLog, ExpenseLog, Assignments
from . import db, mail

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/timelogpage')
def timelog():
    row = TimeLog.query.all()
    return render_template('timelogpage.html', title='Overview', row=row)

@main.route('/add_time', methods=["GET", "POST"])
@login_required
def add_time():
    emp_id = Employee.query.filter_by(user_id=current_user.id).first()
    row = Assignments.query.filter_by(employeeID=emp_id.employeeID)
    if not request.form.get("timeworked") == None:
        tl_var = TimeLog(projectName=request.form.get("projectslist"), employeeID=emp_id.employeeID, currentTime=datetime.datetime.now(), time=request.form.get("timeworked"))
        db.session.add(tl_var)
        db.session.commit()
        flash("New Time Log Successfully Added!")
    return render_template('add_time.html', row=row)

@main.route('/ManageProjects/<prjName>', methods=["GET", "POST"])
@main.route('/ManageProjects/<prjName>/<whatToDo>/<assignmentID>', methods=["GET", "POST"])
@main.route('/ManageProjects/<prjName>/<whatToDo>', methods=["GET", "POST"])
@login_required
def ManageProjects(prjName=None,assignmentID=None,whatToDo=None):
    existing = Employee.query.all()
    if whatToDo =="removeEmployee":
        #existing = Employee.query.all()
        assignmentIDToDelete = Assignments.query.filter_by(AssignmentID=assignmentID).first()
        db.session.delete(assignmentIDToDelete)
        db.session.commit()
        return redirect(url_for('main.ManageProjects', prjName=prjName, title='Overview', existing=existing))

    if whatToDo =="deactivateProject":
       # existing = Employee.query.all()
        projectToDeactivate = Project.query.filter_by(projectName=prjName).first()
        projectToDeactivate.projectOngoing = 0
        db.session.commit()
        return redirect(url_for('main.view_projects', title='Overview', existing=existing))

    if not request.form.get("add_employee_form") == None:
       # existing = Employee.query.all()
        employee_id_var = Assignments(employeeID=request.form.get("add_employee_form"), UserID=current_user.id, projectName=prjName)
        db.session.add(employee_id_var)
        db.session.commit()
        return redirect(url_for('main.ManageProjects', prjName=prjName, title='Overview', existing=existing))

    Tresult = Project.query.filter_by(EmployerID=current_user.id)
    # joinedTables = Assignments.query.join(Employee, Assignments.employeeID==Employee.employeeID).filter_by(projectName="test")
    # q = db.session.query(Employee,Assignments).select_from(Assignments).join(Employee).filter(Assignments.projectName == prjName).all()
    t = text(
        "SELECT * FROM Assignments LEFT JOIN Employees ON Employees.employeeID=Assignments.employeeID WHERE Assignments.projectName = '{}';".format(
            prjName))
    result = db.session.execute(t)
    # print(result.first())
    flash("New Employee Added to Project!")
    return render_template('/ManageProjects.html', prjName=prjName, Tresult=Tresult, EmployeesInProject=result, title='Overview', existing=existing)

@main.route('/addexpense')
@login_required
def addexpense():
    if not current_user.is_employee:
       
    this_employee = Employee.query.filter_by(user_id=current_user.id).first()

    projects = Project.query.filter_by(EmployerID=this_employee.company_id)
    return render_template('addexpense.html', projectsList=projects)


@main.route('/addexpense', methods=['POST'])
@login_required
def addexpense_post():
	if not current_user.is_employee:
		return redirect(url_for('main.profile'))
	this_employee = Employee.query.filter_by(user_id=current_user.id).first()
	this_project = Project.query.filter_by(EmployerID=this_employee.company_id, projectName=request.form.get('projectName')).first()

	e_projectid = this_project.projectID
	e_employeeid = this_employee.employeeID
	e_name=request.form.get("expenseName")
	e_amount=request.form.get("expenseAmount")
	e_description=request.form.get("expenseDescription")
	flash("Expense Successfully Added!")
	expense_entry = ExpenseLog(projectID=e_projectid, employeeID=e_employeeid, expenseName=e_name, expenseAmount=e_amount, expenseDescription=e_description)
	db.session.add(expense_entry)
	db.session.commit()
	return redirect(url_for('main.profile'))

@main.route('/profile')
@login_required
def profile():
    if current_user.is_employee:
        emp_id = Employee.query.filter_by(user_id=current_user.id).first()
        row = Employee.query.filter_by(employeeID=emp_id.employeeID)
        return render_template('profile.html', name=current_user.name, row=row)
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
    flash("New Employee Successfully Invited!")

    # Generate temporary password
    def generate_random_password(length):
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(random.choice(alphabet) for i in range(length))

    temporary_password = generate_random_password(10)

    # Add user,employee to database
    new_user = User(email=email, name=name, password=generate_password_hash(temporary_password, method='sha256'),
                    needs_reset=True, is_employee=True)
    db.session.add(new_user)
    db.session.commit()
    user_entry = User.query.filter_by(email=email).first()
    new_employee = Employee(user_id=user_entry.id, company_id=current_user.id, name=name, emp_email=user_entry.email, jobTitle='Fake Title',
                            payRate=9.00)
    db.session.add(new_employee)
    db.session.commit()

    # Email user that their account has been created
    msg = Message('Account Created', sender='dcaatimemamangement@gmail.com', recipients=[email])
    msg.body = "An account has been created for you. Your temporary password is " + temporary_password + "."
    mail.send(msg)

    return redirect(url_for('main.profile'))

# Edit Employee Info    
@main.route('/editEmployee/<x>', methods=["GET", "POST"])
@login_required
def editEmployee(x=None):

    payrate = request.form.get('payrate')
    name = request.form.get('name')
    title = request.form.get('title')
    user = Employee.query.filter_by(emp_email= x).first()
    user.payRate = payrate
    user.name = name
    user.jobTitle = title
   

    db.session.commit()
    return render_template('editEmployee.html', x = x)


    
@main.route('/employees')
@login_required
def employees():
    if current_user.is_employee:
        redirect(url_for('main.profile'))
    employees = Employee.query.filter_by(company_id=current_user.id)
    return render_template('employees.html', listOfEmployees=employees)


# creates a new project
@main.route('/createProject', methods=["GET", "POST"])
@login_required
def create_project():
    if request.form:
        exists = Project.query.filter_by(projectName=request.form.get("projectNameForm")).first()
        flash("New Project Successfully Created!")
        if not exists:
            project_name_var = Project(projectName=request.form.get("projectNameForm"), projectOngoing=True, EmployerID=current_user.id)
            db.session.add(project_name_var)
            db.session.commit()
    # error message
    return render_template('/createProject.html', name=current_user.name)


# creates
@main.route('/viewProjects', methods=["GET", "POST"])
@login_required
def view_projects():
    projects = Project.query.filter_by(EmployerID=current_user.id)
    return render_template('/ViewProjects.html', name=current_user.name, listOfProjects=projects)

# Audit project
@main.route('/projects/<x>')   
@login_required 
def audit_project(x=None):
    project = Project.query.filter_by(projectID=x).first()
    projectName = project.projectName
    q = ExpenseLog.query.filter_by(projectID=x).join(Employee).add_columns(Employee.emp_email, ExpenseLog.expenseName, ExpenseLog.expenseAmount, ExpenseLog.expenseDescription)
    t = text(
        "SELECT * FROM time_log LEFT JOIN Employees ON Employees.employeeID=time_log.employeeID WHERE time_log.projectName = '{}';".format(
            projectName))
    result = db.session.execute(t)
    return render_template('auditproject.html', query=q, query2=result, projectName=projectName)
