import os
from flask import Flask, render_template, request, redirect, url_for, session
from cs50 import SQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

# قاعدة البيانات
db = SQL("sqlite:///users.db")

# إنشاء الجدول لو مش موجود
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

def rotate(ch,k):
    if ch.isupper():
        c = ord(ch) - ord('A')
        c_i = (k + c) % 26
        return chr(c_i + ord('A'))
    elif ch.islower():
        c = ord(ch) - ord('a')
        c_i = (k + c) % 26
        return chr(c_i + ord('a'))
    else:
        return ch

def code(plain, key):
    cipher = ""
    for ch in plain:
        cipher += rotate(ch, key)
    return cipher


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        first = request.form.get("first_name").strip()
        last = request.form.get("last_name").strip()

        if not first or not last:
            return render_template("login.html", error="Please fill in both fields.")

        # حفظ البيانات
        db.execute("INSERT INTO users (first_name, last_name) VALUES (?, ?)", first, last)

        # حفظ في session
        session["user"] = f"{first} {last}"

        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/home")
def home():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("home.html", user=user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/cipher", methods=["GET", "POST"])
def cipher():
    if request.method == "POST":
        cipher_text = code(request.form.get("plain_text"), int(request.form.get("key")))
        return render_template("cipher.html", cipher_text=cipher_text)
    else:
        return render_template("cipher.html")

@app.route("/snake")
def snake():
    return render_template("snake_game.html")

@app.route("/mouse")
def mouse():
    return render_template("mouse_game.html")

@app.route("/gaza")
def gaza():
    return render_template("gaza.html")


@app.route("/all_users")
def all_users():
    users = db.execute("SELECT * FROM users ORDER BY created_at DESC")
    return render_template("all_users.html", users=users)

if __name__ == "_main_":
    app.run(debug=True)
