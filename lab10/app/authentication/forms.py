from flask_wtf import FlaskForm
from .models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField("Пошта:",
                        validators=[DataRequired("Це поле є обов'язковим"), Email("Будь-ласка введіть ваш пароль")])
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
                       validators=[DataRequired("Це поле обов'язкове"),
                                   Email("Будь ласка, введіть свою електронну адресу")])
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


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Введіть поточний пароль", validators=[DataRequired("Це поле є обов'язковим"),
                                                                    Length(min=4, max=10)])
    newPassword = PasswordField("Введіть новий пароль", validators=[DataRequired("Це поле є обов'язковим"),
                                                                    Length(min=4, max=10)])
    confirmNewPassword = PasswordField("Підтвердіть новий пароль", validators=[DataRequired("Це поле є обов'язковим"),
                                                                               Length(min=4, max=10),
                                                                               EqualTo("newPassword",
                                                                                       "Паролі не збігаються")])
    submit = SubmitField("Скинути")

    def validate_password(self, field):
        if not current_user.checkPassword(field.data):
            raise ValidationError("Невірний пароль")


class UpdateAccountForm(FlaskForm):
    username = StringField("Ім'я користувача", validators=[Length(min=4, max=10),
                                                           Regexp('^[A-Za-z][a-zA-Z0-9._]+$', 0,
                                                                  "Ім'я користувача повинно містити лише букви, цифри, крапки або підкреслення")])
    email = EmailField("Електронна пошта", validators=[Email("Будь ласка, введіть свою електронну адресу")])
    image = FileField('Оновити фото профілю', validators=[FileAllowed(['jpg', 'png'])])
    aboutMe = TextAreaField("Про мене")
    submit = SubmitField("Оновити")

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('Ім\'я користувача вже використовується')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Електронна пошта вже зареєстрована')
