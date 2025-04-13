from flask import Flask
from flask import render_template, session, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import db

app = Flask(__name__)

@app.route("/main")
def index():
    recipelist = db.execute("""SELECT id, title FROM Recipes LIMIT 100""")
    bloglist = db.execute("""SELECT id, title FROM Blogs LIMIT 100""")
    recipe_ids = map(recipelist[0], recipelist)
    recipe_titles = map(recipelist[1], recipelist)
    blog_ids = map(bloglist[0], bloglist)
    blog_titles = map(bloglist[1], bloglist)
    return render_template("main.html", recipes=recipe_titles, blogs=blog_titles)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/confirm", methods=["POST"])
def confirm():
    username = request.form["username_log"]
    password = request.form["password_log"]
    hash = db.execute("""SELECT password_hash 
                      FROM users 
                      WHERE username = ? """, [username]).fetchone()
    if check_password_hash(password, hash):
        session["username"] = username
        return redirect("/main")
    else:
        viesti = "Väärä tunnus tai salasana. Kokeile uudestaan :)"
        return render_template("login.html", i=viesti)
    

@app.route("/uusitili")
def register():
    return render_template("uustili.html")

@app.route("/newacc", methods=["POST"])
def create():
    username = request.form["username_new"]
    password1 = request.form["password_new"]
    password2 = request.form["password_new2"]
    if password1 != password2:
        viesti = "Salasanat eivät ole samat."
        return render_template("uustili.html", i=viesti)
    hash = generate_password_hash(password1)
    try:
        db.execute("""INSERT INTO Users (username, password_hash) 
                   VALUES (?, ?)""", [username, hash])
    except sqlite3.IntegrityError:
        viesti = "Tunnus on jo käytössä"
        return render_template("uustili.html", i=viesti)
    session["username"] = username
    return redirect("/luotu")

@app.route("/eiluotu")
def not_created():
    render_template("eiluotu.html")

@app.route("/luotu")
def created():
    render_template("luotu.html")

@app.route("/haku", methods=["POST"])
def search():
    searched = request.form["searchbar"]
    if searched.isalpha():
        searched_recipes = db.execute("""SELECT r.id, r.title, b.id, b.title 
                                      FROM Recipes r, Blogs b
                                      WHERE b.title = r.title AND r.title = ?
                                      LIMIT 100""", [searched])
    else:
        searched_recipes = db.execute("""SELECT r.id, r.title, b.id, b.title 
                                      FROM Recipes r, Blogs b
                                      WHERE r.id = b.id AND b.id = ?
                                      LIMIT 100""", [searched])
    return render_template("haku.html", results = searched)

@app.route("/profiili")
def profile(): #finish later
    user_id = ("""SELECT id FROM Users WHERE username = ?""", [[session["username"]]])
    recipelist = db.execute("""SELECT id, title FROM Recipes WHERE user_id = ? 
                            LIMIT 100""", [user_id])
    bloglist = db.execute("""SELECT id, title FROM Blogs WHERE user_id = ? 
                            LIMIT 100""", [user_id])
    commentlist = db.execute("""SELECT id, post_id FROM Blogs WHERE user_id = ? 
                            LIMIT 100""", [user_id])
    reviewlist = db.execute("""SELECT id, title FROM Blogs WHERE user_id = ? 
                            LIMIT 100""", [user_id])
    return render_template("profiili.html", recipes = r)

@app.route("/uusresepti")
def recipe():
    return render_template("uusresepti.html")

@app.route("/uusblogi")
def blog():
    return render_template("uusblogi.html")

@app.route("/luoresepti", methods=["POST"])
def new_recipe():
    title = request.form["otsikko"]
    user_id = session["user_id"]
    db.execute("""INSERT INTO Recipes (title, user_id) VALUES (?, ?)""", [title, user_id])
    recipe_id = db.last_insert_id()
    return redirect("/recipes/" + str(recipe_id))
    
@app.route("/recipes/<int:recipe_id>")
def show_recipe(recipe_id: int):
    list = db.execute("""SELECT c.id, c.commenter, c.comment, COUNT(c.id), r.id, r.stars, r.review, COUNT(r.id)
                      FROM Comments c, Reviews r 
                      WHERE c.post_id = r.post_id and c.post_id = ?""", [recipe_id])
    return render_template("resepti.html")

@app.route("/luoblogi", methods=["POST"])
def new_blog():
    title = request.form["otsikko"]
    user_id = session["user_id"]
    db.execute("""INSERT INTO Blogs (title, user_id) VALUES (?, ?)""", [title, user_id])
    blog_id = db.last_insert_id()
    return redirect("/blogs/" + str(blog_id))

@app.route("/blogs/<int:blog_id>")
def show_blog(blog_id: int):
    list = db.execute("""SELECT id, commenter, comment, COUNT(id)
                      FROM Comments
                      WHERE post_id = ?""", [blog_id])
    return render_template("blogi.html")
