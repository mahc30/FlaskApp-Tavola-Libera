from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from tavolalibera.models import Restaurant,Reservation,Security_Question,User, Dish
from tavolalibera.forms import RegisterForm,ReservationForm,LoginForm, CreateRestaurantForm, RequestResetForm, ResetPasswordForm
from tavolalibera import app, db, bcrypt
from datetime import datetime

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

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
            return redirect(url_for("restaurants"))
        else:
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
    else:
        flash("Ocurrió un error. Por favor verifique los datos ingresados", "danger")
        return render_template('register.html', form=form)


       
@app.route('/reservation', methods=["GET", "POST"])
@login_required
def reservation():
    form = ReservationForm()
    restaurant = Restaurant.query.filter_by(name="Miguel").first()
    if request.method == 'GET':
        return render_template('reservation.html', form=form)
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            reservation = Reservation(
            user_id = current_user.id,
            day=form.date.data,
            restaurant_id = restaurant.id,
            start_hour=form.start_time.data,
            finish_hour=form.end_time.data,
            num_people = form.num_people.data,
            )
        else:
            flask("No user login")
        db.session.add(reservation)
        db.session.commit()
        flash("Your reservation has been created successfully!")
        return redirect(url_for("reservation"))
    else:
        flash("Ocurrió un error. Por favor verifique los datos ingresados", "danger")
        return render_template('reservation.html', form=form)

    
    

@app.route('/register/restaurant', methods=['GET', 'POST'])
@login_required
def register_restaurant():
    form = CreateRestaurantForm()
    
    if request.method == 'GET':
        return render_template('register_restaurant.html', form = form)
    
    if form.validate_on_submit():
        restaurant = Restaurant(
            name = form.name.data,
            address = form.address.data,
            phone_number = form.phone_number.data,
            city_id = form.city.data,
            opening_hour = form.opening_hour.data,
            closing_hour = form.closing_hour.data,
            work_days = 'DLMMJVS', #TODO temporal fix, ¿Cómo vamos a guardar los días en que el restaurante está abierto?
            owner_id = current_user.id,
            max_seats = form.max_seats.data
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


@app.route('/restaurant_home/<restaurant_name>', methods=["GET"])
@login_required
def restaurant_home(restaurant_name):
    rst_name = Restaurant.query.filter_by(name=f"{restaurant_name}").first().name
    return render_template('restaurant_home.html',rst_name = rst_name)


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

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.security_answer == form.security_answer.data:
            token = user.get_reset_token()
            return redirect(url_for("reset_token",token=token))
        else:
            flash("La respuesta de seguridad no coincide", "danger")
    return render_template("reset_request.html", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Ese es un token expirado o invalido", "warning")
        return redirect(url_for("reset_request"))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Su contraseña ha sido actualizada correctamente", "info")
        return redirect(url_for("login"))
    return render_template("reset_token.html", form=form)