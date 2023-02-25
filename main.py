from flask import Flask
from flask import render_template
from flaskwebgui import FlaskUI

app = Flask(__name__)
ui = FlaskUI(app=app, server="flask", width=800, height=600)


@app.route('/')
def indexPage():
    return render_template('index.html')


if __name__ == "__main__":
    ui.run()
