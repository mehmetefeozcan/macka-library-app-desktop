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
    bookCode = db.Column(db.String(100), nullable=True)
    bookName = db.Column(db.String(100), nullable=True)
    writer = db.Column(db.String(100), nullable=True)
    page = db.Column(db.String(10), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)


@app.route("/home")
def indexPage():
    return render_template("index.html")


@app.route("/add", methods=["POST", "GET"])
def addBookPage():
    if request.method == "POST" and request.form["btn"] == "Listeye Ekle":
        res = books.query.filter_by(
            bookCode=request.form["bookCode"],
            bookName=request.form["bookName"],
            writer=request.form["writer"],
            page=request.form["page"],
            publisher=request.form["publisher"],
            category=request.form["category"],
        ).first()
        res2 = books.query.filter_by(
            bookCode="100001",
            bookName="Huzur",
            writer=request.form["writer"],
            page=request.form["page"],
            publisher=request.form["publisher"],
            category=request.form["category"],
        ).first()

        if res == None:
            newBook = books(
                bookCode=request.form["bookCode"],
                bookName=request.form["bookName"],
                writer=request.form["writer"],
                page=request.form["page"],
                publisher=request.form["publisher"],
                category=request.form["category"],
            )

            db.session.add(newBook)
            db.session.commit()
            flash("Kitap Başarı ile Eklendi")

    elif request.method == "POST" and request.form["btn"] == "Exceli Ekle":
        print(request.files["ImportExcel"])
        f = request.files["ImportExcel"]
        df1 = pd.read_excel(f, "TÜRK EDEBİYATINDA ROMAN")
        df2 = pd.read_excel(f, "DÜNYA EDEBİYATINDA ROMAN")
        df3 = pd.read_excel(f, "HİKAYE")
        df4 = pd.read_excel(f, "ŞİİR")
        df5 = pd.read_excel(f, "TİYATRO")
        df6 = pd.read_excel(f, "DÜZ YAZI")
        df7 = pd.read_excel(f, "TARİH")
        df8 = pd.read_excel(f, "ATATÜRK KİTAPLARI")
        df9 = pd.read_excel(f, "İNGİLİZCE KİTAPLAR")
        df10 = pd.read_excel(f, "KİŞİSEL GELİŞİM")

        sheets = (df1, df2, df3, df4, df5, df6, df7, df8, df9, df10)
        categories = [
            "Türk Edebiyatında Roman",
            "Dünya Edebiyatında Roman",
            "Hikaye",
            "Şiir",
            "Tiyatro",
            "Düz Yazı",
            "Tarih",
            "Atatürk Kitapları",
            "İngilizce Kitaplar",
            "Kişisel Gelişim",
        ]

        # Kayıt Numarası | Kitabın Adı | Kitabın Yazarı | Sayfa Sayısı | Yayınevi  column names
        for i in range(len(sheets)):
            for index, row in sheets[i].iterrows():
                if (
                    str(row[sheets[i].columns.to_list()[1]]) == "nan"
                    and str(row[sheets[i].columns.to_list()[2]]) == "nan"
                    and str(row[sheets[i].columns.to_list()[3]]) == "nan"
                    and str(row[sheets[i].columns.to_list()[4]]) == "nan"
                ):
                    continue
                newBook = books(
                    bookCode=row[sheets[i].columns.to_list()[0]],
                    bookName=row[sheets[i].columns.to_list()[1]],
                    writer=row[sheets[i].columns.to_list()[2]],
                    page=row[sheets[i].columns.to_list()[3]],
                    publisher=row[sheets[i].columns.to_list()[4]],
                    category=categories[i],
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
