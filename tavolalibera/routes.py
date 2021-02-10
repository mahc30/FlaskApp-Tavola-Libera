from flask import render_template, url_for, redirect, flash, request
from tavolalibera.models import Restaurants,Reservation,Security_Question,User
from tavolalibera.forms import RegisterForm, LoginForm
from tavolalibera import app

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

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("index"))
    return render_template('register.html', form=form)

    """
    if request.method == 'GET':
        
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
    """
