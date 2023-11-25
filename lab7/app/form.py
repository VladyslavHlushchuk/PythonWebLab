from flask_wtf import FlaskForm
from .models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

class LoginForm(FlaskForm):
    email = StringField("Пошта:", validators=[DataRequired("Це поле є обов'язковим"), Email("Будь-ласка введіть ваш пароль")])
    password = PasswordField("Пароль:", validators=[DataRequired("Це поле є обов'язковим"), Length(min=6, max=10)])
    rememberMe = BooleanField("Запам'ятати мене")
    submit = SubmitField("Вхід")


class RegistrationForm(FlaskForm):
    username = StringField("Ім'я користувача", validators=[
        DataRequired("Це поле обов'язкове"),
        Length(min=4, max=10),
        Regexp('^[A-Za-z][a-zA-Z0-9._]+$', 0,
               "Ім'я користувача повинно містити лише літери, цифри, крапки чи підкреслення")])
    email = EmailField("Електронна пошта",
                       validators=[DataRequired("Це поле обов'язкове"), Email("Будь ласка, введіть свою електронну адресу")])
    password = PasswordField("Пароль", validators=[DataRequired("Це поле обов'язкове"), Length(min=6)])
    confirmPassword = PasswordField("Підтвердити пароль", validators=[
        DataRequired("Це поле обов'язкове"),
        EqualTo("password", "Паролі не збігаються")])

    submit = SubmitField("Зареєструватися")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Електронна пошта вже зареєстрована')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ім'я користувача вже використовується")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Введіть новий пароль", validators=[DataRequired("Це поле є обов'язковим"), Length(min=4, max=10)])
    repassword = PasswordField("Введіть новий пароль ще раз", validators=[DataRequired("Це поле є обов'язковим"), Length(min=4, max=10)])
    submit = SubmitField("Змінити")


class AddTodoItemForm(FlaskForm):
    title = StringField("Введіть завдання тут", validators=[DataRequired("Це поле є обов'язковим")])
    description = StringField("Введіть опис тут", validators=[DataRequired("Це поле є обов'язковим")])
    submit = SubmitField("Зберегти")

    class RegistrationForm(FlaskForm):
        username = StringField("Ім'я користувача", validators=[DataRequired("Це поле обов'язкове"), Length(min=4, max=10)])
        email = EmailField("Електронна пошта", validators=[DataRequired("Це поле обов'язкове"), Email("Будь ласка, введіть свою електронну адресу")])
        password = PasswordField("Пароль", validators=[DataRequired("Це поле обов'язкове"), Length(min=6)])
        confirmPassword = PasswordField("Підтвердити пароль", validators=[DataRequired("Це поле обов'язкове"),  EqualTo("password", "Паролі не збігаються")])
        submit = SubmitField("Зареєструватися")