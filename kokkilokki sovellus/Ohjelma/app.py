from flask import Flask
from flask import render_template, session, request
from werkzeug.security import generate_password_hash
import db

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

@app.route("/uustili")
def register():
    return render_template("uustili.html")

@app.route("/tililuotu", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password"]
    password2 = request.form["password again"]
    if password1 != password2:
        viesti = "Salasanat eivät ole samat."
        return render_template("eiluotu.html", message=viesti)
    hash = generate_password_hash(password1)
    try:
        db.execute("""INSERT INTO Users (username, password_hash) 
                   VALUES (?, ?)""", [username, hash])
    except sqlite3.IntegrityError:
        viesti = "Tunnus on jo käytössä"
        return render_template("eiluotu.html", message=viesti)
    return render_template("luotu.html")

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