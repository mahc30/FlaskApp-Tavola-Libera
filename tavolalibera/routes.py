from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from tavolalibera.models import Restaurant ,Reservation ,Security_Question, User, Dish
from tavolalibera.forms import RegisterForm, LoginForm
from tavolalibera import app, db, bcrypt

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html") #Cambiar por Splash

#@app.route('/debug', methods=["GET"])
#def debug():
 
# Cambiar por Splash
# @app.route("/", methods=["GET", "POST"])
# def index():
#    form = LoginForm()
#    return render_template("login.html", form = form)  

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
    flash("Usuario o Contraseña Incorrectos", "danger")
    return render_template("login.html", form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password,security_question=form.security_question.data, security_answer=form.security_answer.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully ! You are now able to login", "info")
        return redirect(url_for("login"))
    else:
        flash("Ocurrió un error. Por favor verifique los datos ingresados")
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/restaurants', methods=["GET"])
@login_required
def restaurants():
   
   restaurants = Restaurant.query.all()
   
   return render_template('restaurants.html', restaurants = restaurants)

@app.route('/dishes/<restaurant_id>', methods=["GET"])
@login_required
def dishes(restaurant_id):
    dishes = Dish.query.filter_by(restaurant_id = restaurant_id)
    
    return render_template('dishes.html', dishes = dishes)