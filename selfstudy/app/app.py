from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Збереження відгуку у базу даних
        new_feedback = Feedback(name=name, email=email, message=message)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Ваш відгук успішно доданий!', 'success')

    # Отримання всіх відгуків з бази даних
    feedbacks = Feedback.query.all()
    return render_template('index.html', feedbacks=feedbacks)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback_to_delete = Feedback.query.get_or_404(id)
    try:
        db.session.delete(feedback_to_delete)
        db.session.commit()
        flash('Відгук успішно видалено!', 'success')
        return redirect('/')
    except:
        flash('Помилка видалення відгуку!', 'danger')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
