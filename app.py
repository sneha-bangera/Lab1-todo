from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect("database.db")
    conn.execute("""
        UPDATE tasks
        SET done = CASE WHEN done=0 THEN 1 ELSE 0 END
        WHERE id=?
    """, (id,))
    conn.commit()
    conn.close()
    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

