from flask import Flask, render_template, url_for, redirect, flash
from controllers.forms import LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "82c021c5452b33eb5c34b1c9abc2e276"


@app.route("/", methods=["GET", "POST"])  # De momento login se encuentra el la raiz
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "jose" and form.password.data == "password":  # Prueba
            flash("You Have Been Logged In", "")
            return redirect(url_for("login"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

