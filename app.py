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
import models #Models imports db so we need to import them AFTER declaring it, interpreted languages go brrr
#Además esto no parecen buenas practicas quizás es mejor usar funciones (?)

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
