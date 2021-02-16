from flask import Flask, render_template

# make the web pages
# make it so we can navigate between the pages via a button
# make [some code] that allows the user to input data on the "create time log" page
# make [some code] that will then take the user inputted data, and store it in the sqlite db
# make [some code] that will then show this newly created entity on the main time log page

app = Flask(__name__)



if __name__ == "__main__":
    app.run()