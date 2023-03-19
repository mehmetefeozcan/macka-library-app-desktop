from flask import *
from flaskwebgui import FlaskUI
from flask_sqlalchemy import *


# flask instance
app = Flask(__name__)
# secret key
app.secret_key = "macka_LIBRARY2023"
# db connect
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./library.db"
# add flaskwebgui
ui = FlaskUI(app=app, server="flask")
# add db
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)


class books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookNo = db.Column(db.String(100), nullable=False)
    bookName = db.Column(db.String(100), nullable=False)
    writer = db.Column(db.String(100), nullable=False)
    page = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)


@app.route("/home")
def indexPage():
    return render_template("index.html")


@app.route("/add", methods=["POST", "GET"])
def addBookPage():
    if request.method == "POST":
        newBook = books(
            bookNo="1",
            bookName="Asd",
            writer="asd",
            page=10,
            publisher="asd",
            category="ŞİİR",
        )

        db.session.add(newBook)
        db.session.commit()
    return render_template("addBook.html")


@app.route("/", methods=["POST", "GET"])
def greet():
    if request.method == "POST":
        if request.form["username"] == "" or request.form["password"] == "":
            flash("Lütfen alanları doldurunuz")

            print("if")
        else:
            try:
                print("try")
                res = user.query.filter_by(
                    username=request.form["username"],
                    password=request.form["password"],
                ).first()

                print(res)
                if res != None:
                    return redirect("/home")
                flash("Hatalı giriş!")

            except Exception:
                print("Exception")
                flash("Kullanıcı bulunamadı")

    return render_template("login.html")  # return render_template("login.html")


if __name__ == "__main__":
    ui.run()
