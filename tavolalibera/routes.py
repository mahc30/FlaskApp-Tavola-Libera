import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from tavolalibera.models import Restaurant,Reservation,Security_Question,User, Dish
from tavolalibera.forms import RegisterForm,ReservationForm,LoginForm, CreateRestaurantForm, UpdateRestaurantForm, RequestResetForm, ResetPasswordForm, CreateDishForm, UpdateDishForm
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
            return redirect(url_for("restaurants"))
        else:
            flash("Usuario o Contraseña Incorrectos", "danger")
            return render_template("login.html", form=form)

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


       
@app.route('/reservation/<restaurant_id>', methods=["GET", "POST"])
@login_required
def reservation(restaurant_id):
    form = ReservationForm()
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
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

@app.route('/redirect/dishes/<restaurant_id>', methods=['GET'])
@login_required
def redirect_dishes(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if restaurant and restaurant.owner_id == current_user.id:
        return redirect(url_for("dishes_admin", restaurant_id=restaurant_id))
    else:
        return redirect(url_for("dishes", restaurant_id=restaurant_id))

@app.route('/redirect/restaurant', methods=['GET'])
@login_required
def redirect_restaurant():
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if restaurant:
        return redirect(url_for("restaurant_home", restaurant_id=restaurant.id))
    else:
        return redirect(url_for("register_restaurant"))

@app.route('/redirect/reservation/<restaurant_id>', methods=['GET'])
@login_required
def redirect_reservation(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if restaurant and restaurant.owner_id == current_user.id:
        return redirect(url_for("reservation_admin", restaurant_id=restaurant.id))
    else:
        return redirect(url_for("reservation", restaurant_id=restaurant.id))

@app.route('/redirect/restaurant_home/<restaurant_id>', methods=['GET'])
@login_required
def redirect_restaurant_home(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if restaurant and restaurant.owner_id == current_user.id:
        return redirect(url_for("restaurant_home_admin",restaurant_id=restaurant.id))
    else:
        return redirect(url_for("restaurant_home", restaurant_id=restaurant.id))


@app.route('/reservation_admin/<restaurant_id>', methods=['GET'])
@login_required
def reservation_admin(restaurant_id):
    books = Reservation.query.filter_by(restaurant_id=restaurant_id)
    return render_template("reservation_admin.html", books=books)


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
        flash("¡El Restaurante se ha creado correctamente!", "info" )
        return redirect(url_for("restaurants"))
    else:
        flash(form.errors, "danger")
        return render_template('register_restaurant.html', form = form)
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route('/restaurant_home_admin/<restaurant_id>', methods=["GET", "POST"])
@login_required
def restaurant_home_admin(restaurant_id):
    form = UpdateRestaurantForm()
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            restaurant.image_url = picture_file
        restaurant.name = form.name.data
        restaurant.description = form.description.data
        db.session.commit()
        flash("your account has been updated!", "success")
        return redirect(url_for("restaurant_home", restaurant_id=restaurant.id))
    elif  request.method == 'GET':
        form.name.data = restaurant.name
        form.description.data = restaurant.description
    
    image_file = url_for("static", filename="img/" + restaurant.image_url)
    return render_template('restaurant_home_admin.html', form=form, restaurant=restaurant, image_file=image_file)

@app.route('/restaurant_home/<restaurant_id>', methods=["GET", "POST"])
@login_required
def restaurant_home(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    image_file = url_for("static", filename="img/" + restaurant.image_url)
    return render_template('restaurant_home.html', restaurant=restaurant, image_file=image_file)
    
    
    

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

@app.route('/dishes_admin/<restaurant_id>', methods=["GET", "POST"])
@login_required
def dishes_admin(restaurant_id):
    form = CreateDishForm()
    # form_update = []
    dishes = Dish.query.filter_by(restaurant_id = restaurant_id)

    # for i in range(len(dishes)):
    #     form_update.push(UpdateDishForm())
    #     form_update[i].dish_id.data = dishes[i].id

    if request.method == 'GET':
        return render_template('dishes_admin.html',form=form,dishes=dishes, restaurant_id=restaurant_id)

    
    if form.validate_on_submit():
        dish = Dish(
            name= form.name.data,
            description = form.description.data,
            restaurant_id = restaurant_id
        )
            
        db.session.add(dish)
        db.session.commit()
        flash("Plato agregado", "info" )
        return redirect(url_for("dishes_admin", restaurant_id=restaurant_id))
    else:
        flash(form.errors, "danger")
        return render_template('dishes_admin.html', form=form,dishes=dishes)

# @app.route('/dishes_admin/<restaurant_id>/<dish_id>', methods=["POST"])
# @login_required
# def dish_admin_post(restaurant_id, dish_id)


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