from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo


# class RegistrationForm(FlaskForm):
#   código


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), InputRequired(), Length(min=2,max=20)])
    password = PasswordField("Contraseña",validators=[DataRequired(),  InputRequired(), EqualTo('confirm_password', message='Las contraseñas deben ser iguales')])
    confirm_password = PasswordField("Confirmar Contraseña",validators=[DataRequired(),  InputRequired()])
    security_question = SelectField("Pregunta de Seguridad", choices=[(1, 'Pregunta 1'), (2, 'Pregunta 2'), (3, 'Pregunta 3')])
    security_answer = StringField("Respuesta", validators=[DataRequired(), InputRequired(), Length(min=2,max=64)])
    submit = SubmitField("Registrarse")
