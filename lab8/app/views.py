from flask import Flask, render_template, request, session, redirect, url_for, make_response, flash
import os
from .form import LoginForm, ChangePasswordForm, AddTodoItemForm, RegistrationForm
from app import app, db
from app.models import Todo, User
from datetime import datetime, timedelta
from os.path import join, dirname, realpath
from flask_login import login_user, current_user, logout_user, login_required
import json




mySkills = [
    {
        "skillName": "HTML",
        "level": "майстерно",
        "icon": "devicon-html5-plain colored fs-45"
    },
    {
        "skillName": "CSS",
        "level": "майстерно",
        "icon": "devicon-css3-plain colored fs-45"
    },
    {
        "skillName": "Python",
        "level": "майстерно",
        "icon": "devicon-python-plain colored fs-45"
    },
    {
        "skillName": "GIT",
        "level": "початківець",
        "icon": "devicon-github-original colored fs-45"
    },
    {
        "skillName": "SQL",
        "level": "досить добре",
        "icon": "fa fa-database fs-45 text-info"
    },
    {
        "skillName": "C++",
        "level": "початківець",
        "icon": "devicon-cplusplus-plain colored fs-45"
    },
    {
        "skillName": "PHP",
        "level": "середній рівень",
        "icon": "devicon-php-plain colored fs-45"
    },
    {
        "skillName": "JavaScript",
        "level": "середній рівень",
        "icon": "devicon-javascript-plain colored fs-45"
    }
]


@app.route("/index")
@app.route('/')
def index():
    osInfo = os.environ.get('OS', 'Unknown OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    show_footer = True
    return render_template('index.html', agent=agent, time=time, osInfo=osInfo, show_footer=show_footer)




@app.route("/contacts")
def contacts():
    show_footer = False
    return render_template('contacts.html', show_footer=show_footer)


@app.route('/skills/<int:id>')
@app.route('/skills')
def skills(id=None):
    osInfo = os.environ['OS']
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")

    if id:
        if id > len(mySkills):
            os.abort()
        else:
            index = id - 1
            skill = mySkills[index]
            return render_template('skill.html', skill=skill, agent=agent, time=time, id=id, osInfo=osInfo)
    else:
        return render_template('skills.html', mySkills=mySkills, agent=agent, time=time, osInfo=osInfo)


@app.route("/study")
def study():
    show_footer = False
    return render_template('study.html', show_footer=show_footer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ви вже ввійшли", "success")
        return redirect(url_for('index'))

    # if session.get('username'):
    #    return redirect(url_for('info'))

    form = LoginForm()

    if form.validate_on_submit():
        inputtedEmail = form.email.data
        inputtedPassword = form.password.data

        user = User.query.filter_by(email=inputtedEmail).first()

        if (inputtedEmail == user.email and user.checkPassword(inputtedPassword)):
            if form.rememberMe.data:
                session["username"] = inputtedEmail
                login_user(user)
                flash("Успішний вхід", "success")
                return redirect(url_for('info'))
            login_user(user)
            flash("Успішний вхід на головну сторінку", "success")
            return redirect(url_for('index'))

        flash("Неправильна  електронна адреса або пароль", "danger")
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash("Ти вже зареєстрований", "success")
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f"Створено акаунт для {form.username.data} !", "success")
        return redirect(url_for('login'))

    return render_template("registration.html", form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/info", methods=['GET', 'POST'])
@login_required
def info():
    changePasswordForm = ChangePasswordForm()

    if not session.get("username"):
        flash("Будь-ласка, відзначте галочку 'запам'ятати мене'", "danger")
        return redirect(url_for('login'))

    username = session.get("username")
    cookies = request.cookies
    return render_template("info.html", username=username, cookies=cookies, changePasswordForm=changePasswordForm)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()
    flash("Ви вийшли з системи", "success")
    return redirect(url_for('login'))


@app.route('/setCookie', methods=["POST"])
def setCookie():
    key = request.form.get("key")
    value = request.form.get("value")
    days = request.form.get("days")
    # message = "Cookie successfully set"
    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=60 * 60 * 24 * int(days))
    return response


@app.route("/deleteCookieByKey", methods=["POST"])
def deleteCookieByKey():
    key = request.form.get("key")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(key)
    return response


@app.route("/deleteCookieAll", methods=["POST"])
def deleteCookieAll():
    cookiesKeys = request.cookies
    response = make_response(redirect(url_for('info')))

    for key, value in cookiesKeys.items():
        if key != "session":
            response.delete_cookie(key)

    return response


@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    changePasswordForm = ChangePasswordForm()

    if changePasswordForm.validate_on_submit():
        newPass = changePasswordForm.password.data
        rePass = changePasswordForm.repassword.data
        username = session.get("username")

        if newPass == rePass:
            dataJsonPath = join(dirname(realpath(__file__)), 'data.json')
            temp = {
                "username": username,
                "password": newPass
            }

            jsonString = json.dumps(temp, indent=2)
            with open(dataJsonPath, "w") as f:
                f.write(jsonString)

            return redirect(url_for('login'))

    return redirect(url_for('info'))


@app.route('/todo', methods=["GET", "POST"])
def todo():
    form = AddTodoItemForm()
    todo_list = Todo.query.all()
    return render_template('todo.html', form=form, todo_list=todo_list)


@app.route('/todo/add', methods=["POST"])
def add():
    form = AddTodoItemForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        todoItem = Todo(title=title, description=description, complete=False)
        db.session.add(todoItem)
        db.session.commit()

    return redirect(url_for("todo"))


@app.route('/todo/delete/<int:id>')
def delete(id):
    todoItem = Todo.query.filter_by(id=id).first_or_404()
    db.session.delete(todoItem)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/todo/update/<int:id>')
def update(id):
    todoItem = Todo.query.filter_by(id=id).first_or_404()
    todoItem.complete = not todoItem.complete
    db.session.commit()
    return redirect(url_for('todo'))

