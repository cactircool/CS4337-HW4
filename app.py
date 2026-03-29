import email
import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev_secret_key"

db_config = {
    "host": "localhost",
    "user": "fxe220002",
    "password": "Ammu272005",
    "database": "company"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        new_password = request.form.get("new_password")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = f"""
            UPDATE users 
            SET password = '{new_password}' 
            WHERE email = '{email}' AND password = '{password}'
            """            
            print("email:", email)
            print("password:", password)
            print("new_password:", new_password)
            print("Generated query:")
            print(query)

            cursor.execute(query)
            conn.commit()

            print("rowcount:", cursor.rowcount)

            cursor.close()
            conn.close()

            if cursor.rowcount > 0:
                flash("Password updated successfully!", "success")
            else:
                flash("Invalid email or password.", "error")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            return f"Database error: {err}"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
