from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


# -------------------------------
# Database Connection Function
# -------------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="YOUR_DB_HOST",
            user="YOUR_DB_USER",
            password="YOUR_DB_PASSWORD",
            database="YOUR_DB_NAME"
        )
        return conn
    except Error as e:
        print("MySQL Connection Error:", e)
        return None


# ------------------------------------------------
# HOME PAGE
# ------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------------------------
# FETCH ALL RECORDS
# ------------------------------------------------
@app.route("/users")
def users():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("users.html", users=rows)


# ------------------------------------------------
# ADD USER
# ------------------------------------------------
@app.route("/add", methods=["POST"])
def add_user():
    name = request.form.get("name")

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name) VALUES (%s)",
        (name,)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("users"))


# ------------------------------------------------
# DELETE USER
# ------------------------------------------------
@app.route("/delete/<int:user_id>")
def delete_user(user_id):

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("users"))


# ------------------------------------------------
# UPDATE USER
# ------------------------------------------------
@app.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    new_name = request.form.get("name")

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=%s WHERE id=%s",
        (new_name, user_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("users"))


# ------------------------------------------------
# START APP
# ------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

