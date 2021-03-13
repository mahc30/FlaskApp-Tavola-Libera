from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from tavolalibera.models import Restaurant,Reservation,Security_Question, User, Dish
from tavolalibera.forms import RegisterForm, LoginForm, CreateRestaurantForm
from tavolalibera import app, db, bcrypt
from datetime import datetime

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

    if request.method == 'GET':
        return render_template("login.html", form=form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
    
    flash("Usuario o Contraseña Incorrectos", "danger")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password,security_question=form.security_question.data, security_answer=form.security_answer.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully ! You are now able to login", "info")
        return redirect(url_for("login"))
    
    flash("Ocurrió un error. Por favor verifique los datos ingresados", "danger")

@app.route('/register/restaurant', methods=['GET', 'POST'])
#@login_required
def register_restaurant():
    form = CreateRestaurantForm()
    
    if request.method == 'GET':
        return render_template('register_restaurant.html', form = form)
    
    if form.validate_on_submit():
        restaurant = Restaurant(
            name = form.name.data,
            address = form.address.data,
            phone_number = form.phone_number.data,
            opening_hour = form.opening_hour.data,
            closing_hour = form.closing_hour.data,
            work_days = 'DLMMJVS', #TODO temporal fix, ¿Cómo vamos a guardar los días en que el restaurante está abierto?
            owner_id = current_user.id
        )
            
        db.session.add(restaurant)
        db.session.commit()
        flash("¡El Restaurante se ha creado correctamente!")
        return render_template('restaurant_home.html')
    else:
        flash(form.errors, "danger")
        return render_template('register_restaurant.html', form = form)
        
        
            
    
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