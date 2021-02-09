import urllib.parse
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from controllers.forms import RegisterForm, LoginForm

# Configure Database URI:
params = urllib.parse.quote_plus(
    "Driver={SQL Server};Server=tcp:tavolalibera.database.windows.net,1433;Database=TavolaLiberaDB;Uid=dreamteam;Pwd=Password1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "82c021c5452b33eb5c34b1c9abc2e276"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_ECHO'] = True

# extensions
db = SQLAlchemy(app)


class Security_Question(db.Model):
    __tablename__ = "security_questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(124), nullable=False)

    def __init__(self, question):
        self.question = question


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(124), nullable=False)
    password = db.Column(db.String(124), nullable=False)
    security_question_id = db.Column(db.Integer,
                                     db.ForeignKey('security_questions.id'),
                                     nullable=False)
    security_question = db.relationship("Security_Question",
                                        backref=db.backref("user",
                                                           uselist=False))
    security_answer = db.Column(db.String(124), nullable=False)

    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password = password
        self.security_question_id = security_question
        self.security_answer = security_answer

    def __repr__(self):
        return f"Username:  {self.username} \nPassword:  {self.password} \nSecurity_Q:  {self.security_question} \nSecurity_A: {self.security_answer}"
        


class Restaurants(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)
    address = db.Column(db.String(124), nullable=False)
    phone_number = db.Column(db.String(124), nullable=False)
    opening_hour = db.Column(db.DateTime, nullable=False)
    closing_hour = db.Column(db.DateTime, nullable=False)
    work_days = db.Column(db.String(124), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User",backref=db.backref("restaurant", uselist=False))

    def __init__(self, name, address, phone_number, opening_hour, closing_hour,
                 work_days):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.work_days = work_days

class Reservation(db.Model):
    __tablename__ = "reservations"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref=db.backref("reservation", uselist=False))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant =  db.relationship("Restaurants", backref=db.backref("reservation", uselist=False))

    __table_args__ = (
    db.PrimaryKeyConstraint(user_id, restaurant_id,),
    )

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
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.username.data == "jose" and form.password.data == "password":  # Prueba
            flash("You Have Been Logged In", "success")
            return redirect(url_for("login"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
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
        user = User(form.username.data, form.password.data,
                    form.security_question.data, form.security_answer.data)

        db.session.add(user)
        db.session.commit()
        flash("Usuario Creado")

        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)


# # DB TEST FUNCTION
# def print_user_names(_db):
#     result = _db.engine.execute("Select {sql} from users")
#     names = [row[1] for row in result]
#     print(names)
