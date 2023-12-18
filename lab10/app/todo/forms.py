from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTodoItemForm(FlaskForm):
    title = StringField("Введіть завдання тут", validators=[DataRequired("Це поле є обов'язковим")])
    description = StringField("Введіть опис тут", validators=[DataRequired("Це поле є обов'язковим")])
    submit = SubmitField("Зберегти")
