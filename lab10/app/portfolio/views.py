import os
from flask import render_template, redirect, url_for, request, abort
from datetime import datetime
from . import portfolio

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


@portfolio.route("/index")
@portfolio.route('/')
def index():
    osInfo = os.environ.get('OS', 'Unknown OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    show_footer = True
    return render_template('index.html', agent=agent, time=time, osInfo=osInfo, show_footer=show_footer)


@portfolio.route("/contacts")
def contacts():
    show_footer = False
    return render_template('contacts.html', show_footer=show_footer)


@portfolio.route('/skills/<int:id>')
@portfolio.route('/skills')
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


@portfolio.route("/study")
def study():
    show_footer = False
    return render_template('study.html', show_footer=show_footer)