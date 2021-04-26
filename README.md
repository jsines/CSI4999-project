# CSI4999-project
DCAA-compliant time management system. This project aims to fulfill the needs to allow companies to record and evaluate time logs and expense logs for projects created under accepted government contracts from the DCAA. For simulating the process, this project is run locally under a python enviornment. All packages needed are in the requirements text, and are automatically installed after opening the project (if in an IDE). Before using the project, you must do the following: 

* If you've made changes to the db structure or need to set it up on your own then go into your python REPL (pytho console) and type the following, one at a time:
  * from project import db, create_app
  * from project.models import *
  * db.create_all(app=create_app())

* To initialize environment variables, Run these in command line and then run "python -m flask run" and the project will then be able to be opened in localhost: 
  * set FLASK_APP=project 
  * set FLASK_DEBUG=1 
  * set MAILPWD=csi4999pass
  

