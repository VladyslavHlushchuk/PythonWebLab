from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача:", validators=[DataRequired("Це поле є обов'язковим")])
    password = PasswordField("Пароль:", validators=[DataRequired("Це поле є обов'язковим"), Length(min=6, max=10)])
    rememberMe = BooleanField("Запам'ятати мене")
    submit = SubmitField("Вхід")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Введіть новий пароль", validators=[DataRequired("Це поле є обов'язковим"), Length(min=4, max=10)])
    repassword = PasswordField("Введіть новий пароль ще раз", validators=[DataRequired("Це поле є обов'язковим"), Length(min=4, max=10)])
    submit = SubmitField("Змінити")


class AddTodoItemForm(FlaskForm):
    title = StringField("Введіть завдання тут", validators=[DataRequired("Це поле є обов'язковим")])
    description = StringField("Введіть опис тут", validators=[DataRequired("Це поле є обов'язковим")])
    submit = SubmitField("Зберегти")