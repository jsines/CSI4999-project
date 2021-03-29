# CSI4999-project
DCAA-compliant time management system

* To initialize environment variables, Run these in command line and then run "python -m flask run" and it should work: 
  * set FLASK_APP=project 
  * set FLASK_DEBUG=1 
  * set MAILPWD=csi4999pass
  

* If you've made changes to the db structure or need to set it up on your own then go into your python REPL and do 
  * from project import db, create_app
  * from project.models import User, [any other tables] (or just * )
  * db.create_all(app=create_app())
