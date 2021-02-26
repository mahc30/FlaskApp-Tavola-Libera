from tavolalibera import db, login_manager
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

    def __repr__(self):
        return f"Username:  {self.username} \nPassword:  {self.password} \nSecurity_Q:  {self.security_question} \nSecurity_A: {self.security_answer}"
        


class Restaurant(db.Model):
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
    # image_url = db.Column(db.String(1024), nullable = True) #TODO migration

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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key = True) #PK
    user = db.relationship("User", backref=db.backref("reservation", uselist=False))
    day = db.Column(db.Date, nullable = False, primary_key = True) #PK
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    start_hour = db.Column(db.DateTime, nullable = False, primary_key = True) #PK
    finish_hour = db.Column(db.DateTime, nullable = False)
    restaurant =  db.relationship("Restaurant", backref=db.backref("reservation", uselist=False))

    __table_args__ = (
    db.PrimaryKeyConstraint(user_id, day, start_hour),
    )
    
class Dish(db.Model):
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    # image_url = db.Column(db.String(1024), nullable=True) #TODO migration
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship("Restaurant", backref=db.backref("dish", uselist=False))
    
    def __init__(self, name, description, restaurant_id):
        self.name = name
        self.description = description
        self.restaurant_id = restaurant_id

# # Create DB
# # This MUST not be in production
print("Creating Tables")
db.create_all()
print("TABLES CREATED")