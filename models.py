from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db

class User(db.Model):
    
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String)
    password = Column(String)
    security_question_id = Column(Integer, ForeignKey('security_questions.id'))
    security_question = relationship("Security_question", backref = backref("user", uselist= False))

    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password = password
        self.security_question_id = security_question
        self.security_answer = security_answer

    def to_string(self):
        string = "Username: " + self.username + "\nPassword: " + self.password + "\nSecurity_Q: " + self.security_question + "\nSecurity_A: " + self.security_answer
        return string

class Security_Question(db.Model):
    __tablename__ = "security_questions"

    id = Column(Integer, primary_key = True)
    question = Column(String)

    def __init__(self, question):
        self.question = question

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref("restaurant", uselist= False))

    def __init__(self, name, address, phone_number, user):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.user = user

db.create_all()