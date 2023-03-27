from flask import *
from flaskwebgui import FlaskUI
from flask_sqlalchemy import *
import pandas as pd


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

    elif request.method == "POST" and request.form["ImportExcel"]:
        print("asdadadasd")
        """with pd.ExcelFile("2022 kitap sayımı günl.xlsx") as xls:
            df1 = pd.read_excel(xls, "TÜRK EDEBİYATINDA ROMAN")
            df2 = pd.read_excel(xls, "DÜNYA EDEBİYATINDA ROMAN")
            df3 = pd.read_excel(xls, "HİKAYE")
            df4 = pd.read_excel(xls, "ŞİİR")
            df5 = pd.read_excel(xls, "TİYATRO")
            df6 = pd.read_excel(xls, "DÜZ YAZI")
            df7 = pd.read_excel(xls, "TARİH")
            df8 = pd.read_excel(xls, "ATATÜRK KİTAPLARI")
            df9 = pd.read_excel(xls, "İNGİLİZCE KİTAPLAR")
            df10 = pd.read_excel(xls, "KİŞİSEL GELİŞİM")

        sheets = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]

        # Kayıt Numarası | Kitabın Adı | Kitabın Yazarı | Sayfa Sayısı | Yayınevi
        for index, row in df1.iterrows():
            if index == 3:
                break
            if (
                str(row["Kitabın Adı"]) == "nan"
                and str(row["Kitabın Yazarı"]) == "nan"
                and str(row["Sayfa Sayısı"]) == "nan"
                and str(row["Yayınevi"]) == "nan"
            ):
                continue
            print(
                index,
                row["Kayıt Numarası"],
                row["Kitabın Adı"],
                row["Kitabın Yazarı"],
                row["Sayfa Sayısı"],
                row["Yayınevi"],
            )
        """
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
