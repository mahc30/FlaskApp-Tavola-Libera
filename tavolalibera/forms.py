from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, ValidationError
from tavolalibera.models import User

class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])

    security_question = SelectField(
        "Security Question", validators=[DataRequired()], choices=[(1, 'Pregunta 1'), (2, 'Pregunta 2'), (3, 'Pregunta 3')]
    )
    security_answer = StringField(
        "Security Answer", validators=[DataRequired(), Length(min=2, max=64)]
    )

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    security_question = SelectField(
        "Security Question", validators=[DataRequired()], choices=[(1, 'Pregunta 1'), (2, 'Pregunta 2'), (3, 'Pregunta 3')]
    )
    security_answer = StringField(
        "Security Answer", validators=[DataRequired(), Length(min=2, max=64)]
    )
    submit = SubmitField("Registrarse")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one")
