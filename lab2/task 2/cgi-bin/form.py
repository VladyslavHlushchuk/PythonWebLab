#!/usr/bin/env python3
import os
import cgi
import http.cookies

missing_fields = []

# Отримання даних з форми
form = cgi.FieldStorage()
name = form.getvalue("name")
email = form.getvalue("email")
language = form.getvalue("language")
experience = form.getvalue("experience")
interests = form.getlist("interests")

if not missing_fields:
    cookies = http.cookies.SimpleCookie()
    cookies["form_count"] = 1  # встановлюємо куки
    print(cookies.output())  # виводимо заголовок Set-Cookie

# Читання cookies
cookies = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
form_count_cookie = cookies.get("form_count")

# Лічильник кількості заповнених форм користувачем
if form_count_cookie:
    form_count = int(form_count_cookie.value)
else:
    form_count = 0

# Збереження cookies з лічильником
cookies["form_count"] = form_count + 1
cookies_output = cookies.output()

# Вивід заголовка з cookies
print(f"Content-type: text/html; charset=utf-8\n{cookies_output}")

# Перевірка, чи всі поля заповнені
missing_fields = []
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
    # Якщо всі поля заповнені, вивести результати опитування та кількість заповнених форм
    print("<h1>Результати опитування</h1>")
    print(f"<p><strong>Ім'я:</strong> {name}</p>")
    print(f"<p><strong>Email:</strong> {email}</p>")
    print(f"<p><strong>Мова програмування:</strong> {language}</p>")
    print(f"<p><strong>Рівень досвіду:</strong> {experience}</p>")
    print(f"<p><strong>Цікавиться:</strong> {', '.join(interests)}</p>")
    print(f"<p><strong>Кількість заповнених форм:</strong> {form_count}</p>")
