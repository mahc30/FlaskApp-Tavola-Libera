<<<<<<< HEAD
import os
import urllib.parse
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from controllers.forms import LoginForm

import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Configure Database URI:
params = urllib.parse.quote_plus(
    "Driver={SQL Server};Server=tcp:tavolalibera.database.windows.net,1433;Database=TavolaLiberaDB;Uid=dreamteam;Pwd=Password1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "82c021c5452b33eb5c34b1c9abc2e276"
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
=======
from flask import Flask, render_template, url_for, redirect, flash, request
from controllers.forms import *
#from models.models import *
import urllib.parse 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configure Database URI: 
params = urllib.parse.quote_plus("Driver={SQL Server};Server=tcp:tavolalibera.database.windows.net,1433;Database=TavolaLiberaDB;Uid=dreamteam;Pwd=Password1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

app = Flask(__name__)
app.config["SECRET_KEY"] = "82c021c5452b33eb5c34b1c9abc2e276"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_ECHO'] = True

>>>>>>> 6fdfe6e7c4c1c017d2a977af40e87b083e130a54

# extensions
db = SQLAlchemy(app)


<<<<<<< HEAD
@app.route("/", methods=["GET", "POST"])  # De momento login se encuentra el la raiz
=======

class Security_Question(db.Model):
    __tablename__ = "security_questions"

    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(124), nullable = False)

    def __init__(self, question):
        self.question = question

class User(db.Model):    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(124), nullable = False)
    password = db.Column(db.String(124), nullable = False)
    security_question_id = db.Column(db.Integer, db.ForeignKey('security_questions.id'), nullable = False)
    security_question = db.relationship("Security_Question", backref = db.backref("user", uselist= False))
    security_answer = db.Column(db.String(124), nullable = False)

    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password = password
        self.security_question_id = security_question
        self.security_answer = security_answer

    def to_string(self):
        string = "Username:  {self.username} \nPassword:  {self.password} \nSecurity_Q:  {self.security_question} \nSecurity_A: {self.security_answer}"
        return string

class Restaurants(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(124), nullable = False)
    address = db.Column(db.String(124), nullable = False)
    phone_number = db.Column(db.String(124), nullable = False)
    opening_hour = db.Column(db.DateTime, nullable = False)
    closing_hour = db.Column(db.DateTime, nullable = False)
    work_days = db.Column(db.String(124), nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    owner = db.relationship("User", backref = db.backref("restaurant", uselist= False))

    def __init__(self, name, address, phone_number, opening_hour, closing_hour, work_days):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.work_days = work_days

# Create DB
# This MUST not be in production
print("Creating Tables")
db.create_all()
print("TABLES CREATED")

@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()

    return render_template("login.html", form=form)


@app.route('/debug', methods=["GET"])
def debug():
    print("DEBUG THIS")
    form = RegisterForm()

    question = Security_Question("Nombre de su mamá")
    db.session.add(question)
    
    question = Security_Question("Nombre de su Papá")
    db.session.add(question)
    question = Security_Question("Nombre de su Primo")
    db.session.add(question)
    db.session.commit()

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"]) 
>>>>>>> 6fdfe6e7c4c1c017d2a977af40e87b083e130a54
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.username.data == "jose" and form.password.data == "password":  # Prueba
            flash("You Have Been Logged In", "")
            return redirect(url_for("login"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
<<<<<<< HEAD

    print_user_names(db)

=======
>>>>>>> 6fdfe6e7c4c1c017d2a977af40e87b083e130a54
    return render_template("login.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        if not form.validate():
            print("Invalid Post")
            print(form.errors)
            return redirect(url_for("register"))
        
        print("INSERTING NEW USER")
        user = User(
            form.username.data,
        form.password.data,
        form.security_question.data,
        form.security_answer.data
        )

        db.session.add(user)
        db.session.commit()
        flash("Usuario Creado")
        
        return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)

<<<<<<< HEAD
# DB TEST FUNCTION
=======

#DB TEST FUNCTION
>>>>>>> 6fdfe6e7c4c1c017d2a977af40e87b083e130a54
def print_user_names(_db):
    result = _db.engine.execute("Select {sql} from users")
    names = [row[1] for row in result]
    print(names)
