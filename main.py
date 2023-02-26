from flask import *
from flaskwebgui import FlaskUI
from flask_sqlalchemy import *


# from model.user_model import *


# flask instance
app = Flask(__name__)
# secret key
app.secret_key = "macka_LIBRARY2023"
# db connect
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./library.db"
# add flaskwebgui
ui = FlaskUI(app=app, server="flask", width=800, height=600)
# add db
db = SQLAlchemy(app)


# User Model
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)


@app.route("/")
def indexPage():
    return render_template("login.html")


@app.route("/greet", methods=["POST", "GET"])
def greet():
    if request.method == "POST":
        if request.form["username"] == "" and request.form["password"] == "":
            flash("Lütfen alanları doldurunuz")
            print("if")
        else:
            print("else")

            findUser = db.one_or_404(
                db.select(user).filter_by(
                    username=request.form["username"], password=request.form["password"]
                )
            )

    return render_template("login.html")


if __name__ == "__main__":
    ui.run()
