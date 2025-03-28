from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk koneksi ke database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Halaman utama (Read)
@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# Halaman tambah data (Create)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        conn = get_db_connection()
        conn.execute("INSERT INTO tasks (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# Halaman edit data (Update)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    
    if request.method == "POST":
        name = request.form["name"]
        conn.execute("UPDATE tasks SET name = ? WHERE id = ?", (name, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    
    conn.close()
    return render_template("edit.html", task=task)

# Hapus data (Delete)
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Jalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
