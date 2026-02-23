
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secretkey"

DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            status TEXT DEFAULT 'Incomplete'
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                    (name,email,password))
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?",
                    (email,password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[0]
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id=?",
                (session["user"],))
    tasks = cur.fetchall()
    conn.close()

    return render_template("dashboard.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    title = request.form["title"]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (user_id,title) VALUES (?,?)",
                (session["user"],title))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/update/<int:id>")
def update(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT status FROM tasks WHERE id=?", (id,))
    status = cur.fetchone()[0]

    new_status = "Completed" if status == "Incomplete" else "Incomplete"

    cur.execute("UPDATE tasks SET status=? WHERE id=?",
                (new_status,id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)