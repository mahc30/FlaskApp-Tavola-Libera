from flask_wtf import FlaskForm
from wtforms import StringField,DateField,TimeField,PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TimeField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, ValidationError, Regexp
from tavolalibera.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
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
            raise ValidationError("Este usuario ya existe, por favor elija otro")



class ReservationForm(FlaskForm):
    date = DateField('Fecha', format='%Y-%m-%d',  validators=[DataRequired()])
    start_time = TimeField("Hora comienzo", validators=[DataRequired()],format='%H:%M')
    end_time = TimeField("Hora finalización", validators=[DataRequired()],format='%H:%M')
    num_people = IntegerField("Cantidad de personas", validators=[DataRequired()])
    lista_platos = SelectField(
        "Agregar platos", validators=[DataRequired()], choices=[(1, ''), (2, ''), (3, '')]
    )
    submit = SubmitField("Book")


class RequestResetForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    security_answer = StringField(
        "Security Answer", validators=[DataRequired(), Length(min=2, max=64)]
    )
    submit = SubmitField("Continuar")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("No existe una cuenta con ese usuario. Registrese primero")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Confirmar")



class CreateRestaurantForm(FlaskForm):
    name = StringField(
        "Nombre del Restaurante", validators=[DataRequired(), Length(min=2, max=64), Regexp(r'^\w+$')]
    )
    address = StringField(
        "Dirección", validators=[DataRequired(), Length(min=2, max=64)]
    )
    phone_number = StringField(
        "Número de teléfono", validators=[DataRequired(), Length(min=2, max=12)]
    )
    city = SelectField(
        "Ciudad", validators=[DataRequired()], choices=[(1, 'Medellín'), (2, 'Bogotá'), (3, 'Dubai')]
    )
    sunday_work_day = BooleanField(
        "sunday_work_day"
    )
    monday_work_day = BooleanField(
        "monday_work_day"
    )
    tuesday_work_day = BooleanField(
        "tuesday_work_day"
    )
    wednesday_work_day = BooleanField(
        "wednesday_work_day"
    )
    thursday_work_day = BooleanField(
        "thursday_work_day"
    )
    friday_work_day = BooleanField(
        "friday_work_day"
    )
    saturday_work_day = BooleanField(
        "saturday_work_day"
    )
    opening_hour = TimeField(
        "Desde", validators = [DataRequired()],format='%H:%M' 
    )
    closing_hour = TimeField(
        "Hasta", validators = [DataRequired()],format='%H:%M' 
    )
    max_seats = IntegerField(
        "Aforo Máximo"
    )
    submit = SubmitField("Completar")

