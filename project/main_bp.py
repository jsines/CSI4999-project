import string, random, datetime, os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from sqlalchemy import text
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .models import User, Employee, Project, TimeLog, ExpenseLog, Assignments, AuditLog
from . import db, mail, UPLOAD_FOLDER
 
main = Blueprint('main', __name__)

# for file uploading
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/timelogpage')
def timelog():
    emp_id = Employee.query.filter_by(user_id=current_user.id).first()
    row = TimeLog.query.filter_by(employeeID=emp_id.employeeID)
    return render_template('timelogpage.html', title='Overview', row=row)

@main.route('/timelogpage/<timelogid>', methods=["GET", "POST"])
@login_required
def deleteTimelog(timelogid=None):
    timelogdelete = TimeLog.query.filter_by(TimeLogID=timelogid).first()
    db.session.delete(timelogdelete)
    db.session.commit()
    # AUDIT TIMELOG DELETED
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    auditdesc = 'Removed TimeLog entry on {} from {} to {}'.format(timelogdelete.startDate, timelogdelete.startTime, timelogdelete.endTime)
    auditlog = AuditLog(time=datetime.date.today(), employerID=employee.company_id, employeeName=timelogdelete.employeeName, projectName=timelogdelete.projectName, description=auditdesc)
    db.session.add(auditlog)
    db.session.commit()
    flash("Time Log Successfully Deleted")
    return timelog()

@main.route('/ExpenseLogs')
def expenseLog():
    emp_id = Employee.query.filter_by(user_id=current_user.id).first()
    row = ExpenseLog.query.filter_by(employeeID=emp_id.employeeID)
    return render_template('ExpenseLogs.html', title='Overview', row=row)

@main.route('/ExpenseLogs/<expenselogid>', methods=["GET", "POST"])
@login_required
def deleteExpenseLog(expenselogid=None):
    expenselogdelete = ExpenseLog.query.filter_by(expenseLogID=expenselogid).first()
    db.session.delete(expenselogdelete)
    db.session.commit()
    this_employee = Employee.query.filter_by(user_id=current_user.id).first()
    this_project = Project.query.filter_by(projectID=expenselogdelete.projectID).first()
    auditdesc = 'Removed Expense entry {} for {} dollars of type {}'.format(expenselogdelete.expenseName, expenselogdelete.expenseAmount, expenselogdelete.expenseType)
    auditlog = AuditLog(time=datetime.date.today(), employerID=this_employee.company_id, employeeName=current_user.name, projectName=this_project.projectName, description=auditdesc)
    db.session.add(auditlog)
    db.session.commit()
    flash("Expense Log Successfully Deleted")
    return expenseLog()

@main.route('/add_time', methods=["GET", "POST"])
@login_required
def add_time():
    emp_id = Employee.query.filter_by(user_id=current_user.id).first()
    row = Assignments.query.filter_by(employeeID=emp_id.employeeID)
    if not request.form.get("starttime") == None:
        project = request.form.get("projectslist")
        start_date = request.form.get("startdate")
        start_time = request.form.get("starttime")
        end_time = request.form.get("endtime")
        tl_var = TimeLog(projectName=project, employeeID=emp_id.employeeID, employeeName=current_user.name, startDate=start_date,startTime=start_time, endTime=end_time, description=request.form.get("description"))
        db.session.add(tl_var)
        db.session.commit()
        # AUDIT TIMELOG ADDED
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        auditdesc = 'Added TimeLog entry on {} from {} to {}'.format(start_date, start_time, end_time)
        auditlog = AuditLog(time=datetime.date.today(), employerID=employee.company_id, employeeName=current_user.name, projectName=project, description=auditdesc)
        db.session.add(auditlog)
        db.session.commit()
        flash("New Time Log Successfully Added!")
    return render_template('add_time.html', row=row, time=datetime.date.today())

@main.route('/ManageProjects/<string:prjName>')
@main.route('/ManageProjects/<string:prjName>/<whatToDo>/<int:employeeID>')
@main.route('/ManageProjects/<string:prjName>/<whatToDo>')
@login_required
def ManageProjects(prjName=None,whatToDo=None,employeeID=None):
    filterEmployeesAvailable = text(
        "SELECT DISTINCT employees.name, employees.employeeID, employees.user_id, employees.emp_email, employees.jobTitle, employees.payRate FROM employees LEFT JOIN assignments ON employees.employeeID=assignments.employeeID WHERE employees.employeeID NOT IN (SELECT assignments.employeeID FROM assignments WHERE assignments.projectName == '{}') OR assignments.projectName IS NULL;".format(prjName))
    existing = db.session.execute(filterEmployeesAvailable)

    Tresult = Project.query.filter_by(EmployerID=current_user.id)
    t = text(
        "SELECT Assignments.assignmentID, employees.employeeID, employees.name, employees.emp_email, employees.jobTitle FROM Assignments LEFT JOIN Employees ON Employees.employeeID=Assignments.employeeID WHERE Assignments.projectName == '{}';".format(prjName))
    result = db.session.execute(t)

    if whatToDo =="removeEmployee":
        assignmentIDToDelete = Assignments.query.filter_by(projectName=prjName, employeeID=employeeID).first()
        db.session.delete(assignmentIDToDelete)
        db.session.commit()
        return redirect(url_for('main.ManageProjects', prjName=prjName, existing=existing))

    if whatToDo =="AddEmployee":
        employee_id_var = Assignments(employeeID=employeeID, UserID=current_user.id, projectName=prjName)
        db.session.add(employee_id_var)
        db.session.commit()
        flash("New Employee Added to Project!")
        return redirect(url_for('main.ManageProjects', prjName=prjName, title='Overview', existing=existing))

    if whatToDo =="deactivateProject":
        projectToDeactivate = Project.query.filter_by(projectName=prjName).first()
        projectToDeactivate.projectOngoing = 0

        db.session.query(Assignments).filter_by(projectName=prjName).delete()
        db.session.commit()
        return redirect(url_for('main.view_projects', title='Overview', existing=existing))

    if whatToDo =="reactivateProject":
        projectToReactivate = Project.query.filter_by(projectName=prjName).first()
        projectToReactivate.projectOngoing = 1
        db.session.commit()
        return redirect(url_for('main.view_projects', title='Overview', existing=existing))

    if not request.form.get("add_employee_form") == None:
        existing = Employee.query.all()
        employee_id_var = Assignments(employeeID=request.form.get("add_employee_form"), UserID=current_user.id, projectName=prjName)
        db.session.add(employee_id_var)
        db.session.commit()
        return redirect(url_for('main.ManageProjects', prjName=prjName, title='Overview', existing=existing))

    Tresult = Project.query.filter_by(EmployerID=current_user.id)
    t = text(
        "SELECT * FROM Assignments LEFT JOIN Employees ON Employees.employeeID=Assignments.employeeID WHERE Assignments.projectName = '{}';".format(
            prjName))
    result = db.session.execute(t)

    projectToManage = Project.query.filter_by(projectName=prjName).first()

    return render_template('/ManageProjects.html', prjName=prjName, Tresult=Tresult, EmployeesInProject=result, title='Overview', existing=existing, projectToManage=projectToManage)

@main.route('/addexpense')
@login_required
def addexpense():
    if not current_user.is_employee:
        return redirect(url_for('main.profile'))
    emp_id = Employee.query.filter_by(user_id=current_user.id).first() #***#
    row = Assignments.query.filter_by(employeeID=emp_id.employeeID) #***#
    return render_template('addexpense.html', projectsList=row)


@main.route('/addexpense', methods=['POST'])
@login_required
def addexpense_post():
    if not current_user.is_employee: # should never happen
        return redirect(url_for('main.profile'))

    this_employee = Employee.query.filter_by(user_id=current_user.id).first()
    this_project = Project.query.filter_by(EmployerID=this_employee.company_id, projectName=request.form.get('projectName')).first()
    
    file = request.files['file']
    e_expenseImg = ''
    if file and allowed_file(file.filename):
        filename = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)))+".png" #random 15 length string
        file.save(os.path.join('project/', UPLOAD_FOLDER, filename))
        e_expenseImg = filename

    e_projectid = this_project.projectID
    e_employeeid = this_employee.employeeID
    e_name=request.form.get("expenseName")
    e_amount=request.form.get("expenseAmount")
    e_description=request.form.get("expenseDescription")
    e_expenseType=request.form.get("expenseType")
    expense_entry = ExpenseLog(projectID=e_projectid, employeeID=e_employeeid, expenseName=e_name, expenseAmount=e_amount, expenseDescription=e_description, expenseType=e_expenseType, expenseImg=e_expenseImg)
    db.session.add(expense_entry)
    db.session.commit()
    # AUDIT EXPENSE ADDED
    auditdesc = 'Added Expense entry {} for {} dollars of type {}'.format(e_name, e_amount, e_expenseType)
    auditlog = AuditLog(time=datetime.date.today(), employerID=this_employee.company_id, employeeName=current_user.name, projectName=this_project.projectName, description=auditdesc)
    db.session.add(auditlog)
    db.session.commit()
    flash("Expense Successfully Added!")
    return redirect(url_for('main.addexpense'))

@main.route('/profile')
@login_required
def profile():
    if current_user.is_employee:
        emp_id = Employee.query.filter_by(user_id=current_user.id).first()
        row = Employee.query.filter_by(employeeID=emp_id.employeeID)
        row2 = Assignments.query.filter_by(employeeID=emp_id.employeeID)
        return render_template('profile.html', name=emp_id.name, row=row, row2=row2)
    return render_template('profile.html', name=current_user.name)

@main.route('/viewEmployee/<x>', methods=["GET"])
@login_required
def viewEmployee(x=None):
    row = Employee.query.filter_by(employeeID=x)
    row2 = Assignments.query.filter_by(employeeID=x)
    return render_template('EmployeeView.html', row=row, row2=row2)

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
    title = request.form.get('title')
    payrate = request.form.get('payrate')
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
    new_employee = Employee(user_id=user_entry.id, company_id=current_user.id, name=name, emp_email=user_entry.email, jobTitle=title,
                            payRate=payrate)
    db.session.add(new_employee)
    db.session.commit()

    # Email user that their account has been created
    msg = Message('Account Created', sender='dcaatimemanagement@gmail.com', recipients=[email])
    msg.body = "An account has been created for you. Your temporary password is " + temporary_password + "."
    mail.send(msg)

    return redirect(url_for('main.invite'))

@main.route('/editEmployee/<x>')
@login_required
def editEmployee(x=None):
    return render_template('editEmployee.html', x = x)

# Edit Employee Info
@main.route('/editEmployee/<x>', methods=["POST"])
@login_required
def editEmployeepost(x=None):

    payrate = request.form.get('payrate')
    name = request.form.get('name')
    title = request.form.get('title')
    user = Employee.query.filter_by(emp_email= x).first()
    user.payRate = payrate
    user.name = name
    user.jobTitle = title
   

    db.session.commit()
    flash("New Employee Info Saved!")
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
@main.route('/projects/<x>/<expenseid>')
@main.route('/projects/<x>')   
@login_required 
def audit_project(x=None, expenseid=None):


    project = Project.query.filter_by(projectID=x).first()
    projectName = project.projectName
    q = ExpenseLog.query.filter_by(projectID=x).join(Employee).add_columns(Employee.emp_email, ExpenseLog.expenseName, ExpenseLog.expenseAmount, ExpenseLog.expenseDescription, ExpenseLog.expenseType, ExpenseLog.expenseImg, ExpenseLog.projectID, ExpenseLog.expenseLogID)
    t = text(
        "SELECT * FROM time_log LEFT JOIN Employees ON Employees.employeeID=time_log.employeeID WHERE time_log.projectName = '{}';".format(
            projectName))
    result = db.session.execute(t)

    # Remove Expense
    if not expenseid == None:
        delexpense = ExpenseLog.query.filter_by(expenseLogID=expenseid).first()
        db.session.delete(delexpense)
        db.session.commit()
        flash("Expense Successfully Deleted.")
        this_employee = Employee.query.filter_by(user_id=current_user.id).first()
        this_project = Project.query.filter_by(projectID=delexpense.projectID).first()
        auditdesc = 'Removed Expense entry {} for {} dollars of type {}'.format(delexpense.expenseName, delexpense.expenseAmount, delexpense.expenseType)
        auditlog = AuditLog(time=datetime.date.today(), employerID=current_user.id, employeeName=current_user.name, projectName=this_project.projectName, description=auditdesc)
        db.session.add(auditlog)
        db.session.commit()
        return redirect(url_for('main.audit_project', x=x))

    return render_template('auditproject.html', query=q, query2=result, projectName=projectName)

@main.route('/audit')
@login_required
def audit():
    auditlogs = AuditLog.query.filter_by(employerID=current_user.id)
    return render_template('audit.html', auditLogs=auditlogs)

# Display receipts
@main.route('/receipts/<filename>')
@login_required
def display_receipt(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
