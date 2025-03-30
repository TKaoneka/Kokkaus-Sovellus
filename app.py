from flask import Flask
from flask import render_template
import dbase

app = Flask(__name__)

@app.route("/main")
def index():
    recipelist = User.search_recipes("")
    ids = []
    titles = []
    for i in recipelist:
        ids.append(i[0])
        titles.append(i[1])
    return render_template("main.html", recipes=titles)

@app.route("/profiili")
def profile():
    username = request.form[""]
    recipelist = User.search_recipes()
    ids = []
    titles = []
    for i in recipelist:
        ids.append(i[0])
        titles.append(i[1])
    return render_template("main.html", recipes=titles)