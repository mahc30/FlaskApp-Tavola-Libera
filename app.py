import os
import urllib.parse
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from controllers.forms import LoginForm

params = urllib.parse.quote_plus(
    "Driver={​​​​SQL Server}​​​​;Server=tcp:tavolalibera.database.windows.net,1433;Database=TexitberaDB;Uid=dreamteam;Pwd=Password1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)


app = Flask(__name__)

app.config["SECRET_KEY"] = "82c021c5452b33eb5c34b1c9abc2e276"
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % params
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])  # De momento login se encuentra el la raiz
def login():
    form = LoginForm()
    results = db.engine.execute("select * from users")
    if form.validate_on_submit():
        if form.username.data == "jose" and form.password.data == "password":  # Prueba
            flash("You Have Been Logged In", "")
            return redirect(url_for("login"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")

    return render_template("login.html", form=form, results=results)


if __name__ == "__main__":
    app.run(debug=True)

