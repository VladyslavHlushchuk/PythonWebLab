#!/usr/bin/env python3
print("Content-type: text/html; charset=utf-8\n")

import cgi

form = cgi.FieldStorage()

# Отримання даних з форми
name = form.getvalue("name")
email = form.getvalue("email")
language = form.getvalue("language")
experience = form.getvalue("experience")
interests = form.getlist("interests")

# Список для збереження незаповнених полів
missing_fields = []

# Перевірка, чи всі поля заповнені
if not name:
    missing_fields.append("Ім'я")
if not email:
    missing_fields.append("Email")
if not language:
    missing_fields.append("Мова програмування")
if not experience:
    missing_fields.append("Рівень досвіду")
if not interests:
    missing_fields.append("Цікавості")

if missing_fields:
    # Якщо є незаповнені поля, вивести повідомлення про незаповнені поля
    print("<h1>Помилка: Будь ласка, заповніть наступні поля:</h1>")
    print("<ul>")
    for field in missing_fields:
        print(f"<li>{field}</li>")
    print("</ul>")
else:
    # Якщо всі поля заповнені, вивести результати опитування
    print("<h1>Результати опитування</h1>")
    print(f"<p><strong>Ім'я:</strong> {name}</p>")
    print(f"<p><strong>Email:</strong> {email}</p>")
    print(f"<p><strong>Мова програмування:</strong> {language}</p>")
    print(f"<p><strong>Рівень досвіду:</strong> {experience}</p>")
    print(f"<p><strong>Цікавиться:</strong> {', '.join(interests)}</p>")