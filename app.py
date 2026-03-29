import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MySQL connection config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "cactircool",
    "database": "hw4"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
            print(query)
            cursor.execute(query)
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                return f"Welcome, {user['email']}!"
            else:
                flash("Invalid email or password")

        except mysql.connector.Error as err:
            return f"Database error: {err}"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
