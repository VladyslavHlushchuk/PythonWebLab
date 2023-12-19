from flask import url_for
from flask_login import current_user
from app import db
from app.authentication.models import User
from app.post.models import Post


def test_all_posts_page_loads(client):
    response = client.get(url_for('post.posts'))
    assert response.status_code == 200
    assert u'Список постів' in response.data.decode('utf8')


def test_post_create_page_loads(client):
    response = client.get(url_for('post.create'))
    assert response.status_code == 200
    assert u'Створити новий пост' in response.data.decode('utf8')


def test_post_edit_page_loads(client, init_database):
    response = client.get(url_for('post.update', id=1))
    assert response.status_code == 200
    assert u'Редагувати пост' in response.data.decode('utf8')