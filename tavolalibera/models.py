from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tavolalibera import db, login_manager, app
from flask_login import  UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Security_Question(db.Model):
    __tablename__ = "security_questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(124), nullable=False)

    def __init__(self, question):
        self.question = question


class User(db.Model, UserMixin):
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
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Username:  {self.username} \nPassword:  {self.password} \nSecurity_Q:  {self.security_question} \nSecurity_A: {self.security_answer}"
        


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)
    address = db.Column(db.String(124), nullable=False)
    phone_number = db.Column(db.String(124), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable = False)
    city = db.relationship("City", backref = db.backref("restaurant", uselist= False))
    opening_hour = db.Column(db.Time, nullable=False)
    closing_hour = db.Column(db.Time, nullable=False)
    work_days = db.Column(db.String(124), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User",backref=db.backref("restaurant", uselist=False))
    max_seats = db.Column(db.Integer, nullable = False)
    image_url = db.Column(db.String(1024), nullable=True, default="https://via.placeholder.com/300")
    
    def __init__(self, name, address, phone_number, city_id, opening_hour, closing_hour, work_days, owner_id, max_seats):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.city_id = city_id
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.work_days = work_days
        self.owner_id = owner_id
        self.max_seats = max_seats

class Reservation(db.Model):
    __tablename__ = "reservations"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key = True) #PK
    user = db.relationship("User", backref=db.backref("reservation", uselist=False))
    day = db.Column(db.Date, nullable = False, primary_key = True) #PK
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    start_hour = db.Column(db.DateTime, nullable = False, primary_key = True) #PK
    finish_hour = db.Column(db.DateTime, nullable = False)
    #num_people = (db.Integer,nullable = False)
    restaurant =  db.relationship("Restaurant", backref=db.backref("reservation", uselist=False))

    __table_args__ = (
    db.PrimaryKeyConstraint(user_id, day, start_hour),
    )
    
class Dish(db.Model):
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    image_url = db.Column(db.String(1024), nullable=True, default="https://via.placeholder.com/300")
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship("Restaurant", backref=db.backref("dish", uselist=False))
    
    def __init__(self, name, description, restaurant_id):
        self.name = name
        self.description = description
        self.restaurant_id = restaurant_id

class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)
    
# # Create DB
# # This MUST not be in production
# print("Creating Tables")
 #db.create_all()
# print("TABLES CREATED")