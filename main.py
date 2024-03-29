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

selectedCategory = ""


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
    isGiven = db.Column(db.Boolean, default="False", nullable=False)


class members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(10), nullable=False)
    no = db.Column(db.String(10), nullable=False)


class givenBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    bookCode = db.Column(db.String(100), nullable=False)
    bookName = db.Column(db.String(100), nullable=False)
    studentName = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(10), nullable=False)
    no = db.Column(db.String(10), nullable=False)


# for the table create
""" with app.app_context():
    db.create_all() """


@app.route("/home", methods=["POST", "GET"])
def indexPage():
    selectedCategory = ""
    if request.method == "POST":
        selectedCategory = request.form["category"]

        return redirect(url_for(".booksPage", category=selectedCategory))
    return render_template("index.html")


@app.route("/books", methods=["POST", "GET"])
def booksPage():
    selectedCategory = request.args["category"]
    if selectedCategory == "Düzyazı":
        selectedCategory = "Düz Yazı"

    if selectedCategory == "Tümü":
        response = books.query.all()
    elif selectedCategory == "Verilen Kitaplar":
        return redirect("/given-books")
    else:
        response = books.query.filter_by(
            category=selectedCategory,
        ).all()

    if request.method == "POST":
        _code = request.form["Sil"]

        books.query.filter_by(bookCode=_code).delete()
        response = books.query.filter_by(
            category=selectedCategory,
        ).all()
        db.session.flush()
        db.session.commit()

        return render_template("books.html", books=response, category=selectedCategory)

    return render_template("books.html", books=response, category=selectedCategory)


# verilen kitaplar sayfası
@app.route("/given-books", methods=["POST", "GET"])
def givenBooksPage():
    _givenBooks = givenBooks.query.all()

    if request.method == "POST":
        _code = request.form["iade"]

        givenBooks.query.filter_by(bookCode=_code).delete()
        _resbook = books.query.filter_by(bookCode=_code).first()

        _resbook.isGiven = False

        db.session.flush()
        db.session.commit()

        return redirect("/given-books")

    return render_template("givenBooks.html", givenBooks=_givenBooks)


# kitap verme sayfası
@app.route("/give-book", methods=["POST", "GET"])
def giveBookPage():
    bookRes = books.query.filter_by(isGiven=False).all()
    memberRes = members.query.all()

    if request.method == "POST":
        if request.form["member"] == "" or request.form["book"] == "":
            flash("Lütfen tüm alanları doldurunuz !")
        else:
            _bookCode = request.form["book"].split("-")[0]
            _memberNo = request.form["member"].split("-")[0]

            _resbook = books.query.filter_by(bookCode=_bookCode).first()
            _resMember = members.query.filter_by(no=_memberNo).first()

            newReq = givenBooks(
                category=_resbook.category,
                bookCode=_resbook.bookCode,
                bookName=_resbook.bookName,
                studentName=str("{} {}".format(_resMember.name, _resMember.surname)),
                classroom=_resMember.classroom,
                no=_resMember.no,
            )
            _resbook.isGiven = True
            db.session.add(newReq)
            db.session.flush()
            db.session.commit()

            flash("Başarıyla Eklendi !")

            return redirect("/give-book")
    return render_template("giveBook.html", books=bookRes, members=memberRes)


# üye ekleme sayfası
@app.route("/add-member", methods=["POST", "GET"])
def memberPage():
    _members = members.query.all()

    if request.method == "POST":
        if "btn" in request.form:
            if (
                request.form["memberName"] == ""
                or request.form["classroom"] == ""
                or request.form["memberSurname"] == ""
                or request.form["memberNumber"] == ""
            ):
                flash("Lütfen tüm alanları doldurunuz !")
            else:
                res = members.query.filter_by(
                    no=request.form["memberNumber"],
                ).first()

                if res == None:
                    newMember = members(
                        name=request.form["memberName"],
                        surname=request.form["memberSurname"],
                        classroom=request.form["classroom"],
                        no=request.form["memberNumber"],
                    )

                    db.session.add(newMember)
                    db.session.commit()

                    _members = members.query.all()
                    redirect("/add-member")
                else:
                    flash("Zaten böyle bir üye var!")
        if "Sil" in request.form:
            _no = request.form["Sil"]

            members.query.filter_by(no=_no).delete()

            db.session.flush()
            db.session.commit()
            _members = members.query.all()
            redirect("/add-member")

    return render_template("addMember.html", members=_members)


# kitap ekleme sayfası
@app.route("/add", methods=["POST", "GET"])
def addBookPage():
    if request.method == "POST" and request.form["btn"] == "Kitabı Ekle":
        if (
            request.form["bookCode"] == ""
            or request.form["bookName"] == ""
            or request.form["writer"] == ""
            or request.form["page"] == ""
            or request.form["publisher"] == ""
            or request.form["category"] == ""
        ):
            flash("Lütfen tüm alanları doldurunuz !")
        else:
            res = books.query.filter_by(
                bookCode=request.form["bookCode"],
            ).first()

            if res == None:
                newBook = books(
                    bookCode=request.form["bookCode"],
                    bookName=request.form["bookName"],
                    writer=request.form["writer"],
                    page=request.form["page"].split(".")[0],
                    publisher=request.form["publisher"],
                    category=request.form["category"],
                    isGiven=False,
                )

                db.session.add(newBook)
                db.session.commit()
                flash("Kitap Başarı ile Eklendi")
            else:
                flash("Aynı Bilgilerde Kitap Bulundu.")

    elif request.method == "POST" and request.form["btn"] == "Exceli Ekle":
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

                _code = 0

                try:
                    _code = row["Kayıt Numarası"].split(".")[0]
                except Exception:
                    _code = row["Kayıt Numarası"]

                res = books.query.filter(
                    books.bookCode == _code,
                ).first()
                print(res)
                if res == None:
                    newBook = books(
                        bookCode=str(row[sheets[i].columns.to_list()[0]]).split(".")[0],
                        bookName=row[sheets[i].columns.to_list()[1]],
                        writer=row[sheets[i].columns.to_list()[2]],
                        page=str(row[sheets[i].columns.to_list()[3]]).split(".")[0],
                        publisher=row[sheets[i].columns.to_list()[4]],
                        category=categories[i],
                        isGiven=False,
                    )

                    db.session.add(newBook)
                    db.session.commit()
                else:
                    continue

    return render_template("addBook.html")


# login sayfası
@app.route("/", methods=["POST", "GET"])
def greet():
    if request.method == "POST":
        if request.form["username"] == "" or request.form["password"] == "":
            flash("Lütfen tüm alanları doldurunuz")

        else:
            try:
                res = user.query.filter_by(
                    username=request.form["username"],
                    password=request.form["password"],
                ).first()

                if res != None:
                    return redirect("/home")
                flash("Hatalı giriş!")

            except Exception:
                flash("Kullanıcı bulunamadı")

    return render_template("login.html")


if __name__ == "__main__":
    ui.run()
