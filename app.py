from flask import Flask
from flask import render_template, session, request, redirect, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "id" not in session:
        abort(403)

@app.route("/")
def index():
    recipes = db.query("""SELECT * FROM Recipes LIMIT 100""")
    blogs = db.query("""SELECT * FROM Blogs LIMIT 100""")
    
    return render_template("main.html", recipes=recipes, blogs=blogs)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registration")
def registeration():
    return render_template("uustili.html")

@app.route("/confirm", methods=["POST"])
def confirm():
    username = request.form["username_log"]
    password = request.form["password_log"]
    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    try:
        info = db.query(sql, [username])[0]
    except IndexError:
        viesti = "Väärä tunnus tai salasana. Kokeile uudestaan :)"
        return render_template("login.html", i=viesti)
    
    if check_password_hash(info[1], password):
        session["username"] = username
        session["id"] = info[0]
        return redirect("/")
    else:
        viesti = "Väärä tunnus tai salasana. Kokeile uudestaan :)"
        return render_template("login.html", i=viesti)

@app.route("/register", methods=["POST"])
def create():
    username = request.form["username_new"]
    password1 = request.form["password_new"]
    password2 = request.form["password_new2"]
    if password1 != password2:
        viesti = "Salasanat eivät ole samat. Ole hyvä ja kokeile uudestaan"
        return render_template("uustili.html", i=viesti)
    hash = generate_password_hash(password1)
    try:
        db.execute("""INSERT INTO Users (username, password_hash) 
                   VALUES (?, ?)""", [username, hash])
    except sqlite3.IntegrityError:
        viesti = "Tunnus on jo käytössä. Ole hyvä ja kokeile uudestaan"
        return render_template("uustili.html", i=viesti)
    session["username"] = username
    session["id"] = db.query("""SELECT id FROM Users WHERE username = ?""", [username])[0][0]
    return render_template("luotu.html")

@app.route("/logout")
def logout():
    del session["username"]
    del session["id"]
    return redirect("/")

@app.route("/search")
def search():
    searched = request.args.get("searchbar")
    if searched.isalpha():
        sql1 = """SELECT r.id, r.title,
        b.id blogid, b.title blogtitle
        FROM Recipes r, Blogs b
        WHERE b.title LIKE ? AND r.title LIKE ?
        LIMIT 100"""
    else:
        sql1 = """SELECT r.id, r.title,
        b.id blogid, b.title blogtitle
        FROM Recipes r, Blogs b
        WHERE b.id LIKE ? OR r.id LIKE ?
        LIMIT 100"""

    searched_posts = db.query(sql1, ["%" + searched + "%", "%" + searched + "%"]) if searched else []
     
    return render_template("haku.html", results = searched_posts, searchbar = searched)

@app.route("/profile/<int:user_id>")
def show_profile(user_id):
    sql1 = """SELECT username, image IS NOT NULL has_pfp FROM Users WHERE id = ?"""
    sql2 = """SELECT id, title, time_posted 
    FROM Recipes WHERE user_id = ? 
    ORDER BY time_posted DESC"""

    sql3 = """SELECT id, title, time_posted 
    FROM Blogs WHERE user_id = ? 
    ORDER BY time_posted DESC"""

    sql4 = """SELECT c.post, c.comment, c.time_posted, b.title
    FROM Comments c, Blogs b WHERE c.post = b.id AND c.commenter = ? 
    ORDER BY c.time_posted DESC"""

    sql5 = """SELECT r.post, r.stars, r.time_posted, a.title, a.image thumbnail
    FROM Reviews r, Recipes a WHERE r.post = a.id AND r.reviewer = ? 
    ORDER BY r.time_posted DESC"""

    sql6 = """SELECT 
    (SELECT COUNT(*) FROM Recipes WHERE user_id = ?) rtotal,
    (SELECT COUNT(*) FROM Blogs WHERE user_id = ?) btotal,
    (SELECT COUNT(*) FROM Comments WHERE commenter = ?) ctotal,
    (SELECT COUNT(*) FROM Reviews WHERE reviewer = ?) atotal,
    (SELECT AVG(stars) FROM Reviews WHERE reviewer = ?) avg"""

    owner = db.query(sql1, [user_id])
    recipes = db.query(sql2, [user_id])
    blogs = db.query(sql3, [user_id])
    comments = db.query(sql4, [user_id])
    reviews = db.query(sql5, [user_id])
    totals = db.query(sql6, [user_id, user_id, user_id, user_id, user_id])
     
    return render_template("profiili.html", user=owner[0], user_id=user_id, recipes=recipes, blogs=blogs,
                            reviews=reviews, comments=comments, totals=totals[0])

@app.route("/add_photo", methods = ["GET", "POST"])
def add_photo():
    require_login()

    if request.method == "GET":
        return render_template("add_photo.html")

    if request.method == "POST":
        file = request.files["photo"]
        if not file.filename.endswith(".jpg"):
            message = "Väärä tiedostomuoto"
            return render_template("add_photo.html", i=message)
        pfp = file.read()
        if len(pfp) > 100 * 1024:
            message = "Kuva on liian suuri"
            return render_template("add_photo.html", i=message)
        sql = """UPDATE Users SET image = ? WHERE id = ?"""
        db.execute(sql, [pfp, session["id"]])
        return redirect(f"/profile/{session["id"]}")
    
@app.route("/photo/<int:user_id>")
def show_pfp(user_id):
    sql = """SELECT image FROM Users WHERE id = ?"""
    pfp = db.query(sql, [user_id])[0][0]
    if not pfp:
        abort(404)

    response = make_response(bytes(pfp))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/thumbnail/<int:recipe_id>")
def show_thumbnail(recipe_id):
    sql = """SELECT image FROM Recipes WHERE id = ?"""
    thumbnail = db.query(sql, [recipe_id])[0][0]
    if not thumbnail:
        abort(404)

    response = make_response(bytes(thumbnail))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/new_recipe", methods=["GET", "POST"])
def recipe():
    require_login()

    if request.method == "GET":
        return render_template("uusresepti.html")
    
    if request.method == "POST":
        title = request.form["title"]

        thumbnail = request.files["thumbnail"]
        photo = thumbnail.read()
        if len(photo) > 100 * 1024:
            message = "Kuva on liian suuri!"
            return message
        
        sql1 = """INSERT INTO Recipes (title, user_id, time_posted, image)
        VALUES (?, ?, datetime('now'), ?)"""
        db.execute(sql1, [title, session["id"], photo])
        recipe_id = db.last_insert_id()

        preptimeh = request.form["preptimeh"]
        preptimem = request.form["preptimem"]
        cooktimeh = request.form["cooktimeh"]
        cooktimem = request.form["cooktimem"]

        steps = request.form["steps"]
        ingredients = request.form["ingredients"]
        sql2 = """INSERT INTO recipe_details (preptimeh, preptimem, cooktimeh, 
        cooktimem, ingredients, steps, recipe)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
        db.execute(sql2, [preptimeh, preptimem, cooktimeh, cooktimem, ingredients ,len(steps), recipe_id])

        split = steps.split(", ")
        sql3 = """INSERT INTO recipe_steps (step, place, recipe)
        VALUES (?, ?, ?)"""
        for i in split:
            db.execute(sql3, [i, split.index(i)+1, recipe_id])
        
        return redirect(f"/recipe/{str(recipe_id)}")
    
@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    sql1 = """SELECT * FROM Recipes WHERE id = ?"""
    sql2 = """SELECT a.id, a.reviewer, a.stars, a.review, a.time_posted,
    u.username, u.image IS NOT NULL has_pfp
    FROM Reviews a, Users u 
    WHERE a.post = ? AND a.reviewer = u.id
    ORDER BY a.time_posted DESC"""
    sql3 = """SELECT COUNT(*) total, AVG(stars) avg
    FROM Reviews WHERE post = ?"""
    sql4 = """SELECT * FROM recipe_details WHERE recipe = ?"""
    sql5 = """SELECT * FROM recipe_steps WHERE recipe = ?
    ORDER BY place ASC"""
    sql6 = """SELECT username FROM Users WHERE id = ?"""

    recipe = db.query(sql1, [recipe_id])
    reviews = db.query(sql2, [recipe_id])
    totals = db.query(sql3, [recipe_id])
    details = db.query(sql4, [recipe_id])
    steps = db.query(sql5, [recipe_id])
    user = db.query(sql6, [recipe[0][2]])

    return render_template("resepti.html", recipe=recipe[0], user=user[0][0], steps=steps, totals=totals[0], reviews=reviews, details=details[0])

@app.route("/new_blog")
def blog():
    require_login()
    return render_template("uusblogi.html")

@app.route("/makeblog", methods=["POST"])
def new_blog():
    title = request.form["otsikko"]
    text = request.form["blogtext"]
    db.execute("""INSERT INTO Blogs (title, content, user_id, time_posted) 
               VALUES (?, ?, ?, datetime('now'))""", [title, text, session["id"]])
    blog_id = db.last_insert_id()
    return redirect(f"/blog/{str(blog_id)}")

@app.route("/blog/<int:blog_id>")
def show_blog(blog_id):
    sql1 = """SELECT * FROM Blogs WHERE id = ?"""
    sql2 = """SELECT username, image IS NOT NULL has_pfp FROM Users WHERE id = ?"""
    sql3 = """SELECT c.id, c.commenter, c.comment, c.time_posted, 
    u.username, u.image IS NOT NULL has_pfp
    FROM Comments c, Users u 
    WHERE c.post = ? AND c.commenter = u.id
    ORDER BY c.time_posted DESC"""
    sql4 = """SELECT COUNT(c.id) FROM Comments c, Users u
    WHERE c.post = ? AND c.commenter = u.id"""
    blog = db.query(sql1,[blog_id])
    writer = db.query(sql2,[blog[0][3]])
    comments = db.query(sql3,[blog_id])
    total = db.query(sql4,[blog_id])
    return render_template("blogi.html", blog=blog[0], user=writer, comments=comments, total=total[0][0])

@app.route("/edit_blog/<int:blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    sql = """SELECT title, content FROM Blogs WHERE id = ?"""
    edited = db.query(sql, [blog_id])
    if request.method == "GET":
        return render_template("editblog.html", blog_id=blog_id, blog=edited[0])
    elif request.method == "POST":
        text = request.form["editedtext"]
        sql = """UPDATE Blogs SET content = ? WHERE id = ?"""
        db.execute(sql, [text, blog_id])
        return redirect(f"/blog/{blog_id}")
    
@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    if request.method == "GET":
        return render_template("removerecipe.html", recipe_id=recipe_id)
    
    elif request.method == "POST":
        if "continue" in request.form:
            sql1 = """DELETE FROM Recipes WHERE id = ?"""
            sql2 = """DELETE FROM recipe_details WHERE recipe = ?"""
            sql3 = """DELETE FROM recipe_steps WHERE recipe = ?"""
            db.execute(sql3, [recipe_id])
            db.execute(sql2, [recipe_id])
            db.execute(sql1, [recipe_id])
            return redirect("/")
        elif "cancel" in request.form:
            return redirect(f"/recipe/{recipe_id}")
    
@app.route("/remove_blog/<int:blog_id>", methods=["GET", "POST"])
def remove_blog(blog_id):
    if request.method == "GET":
        return render_template("removeblog.html", blog_id=blog_id)
    
    elif request.method == "POST":
        if "continue" in request.form:
            sql = """DELETE FROM Blogs WHERE id = ?"""
            db.execute(sql, [blog_id])
            return redirect("/")
        elif "cancel" in request.form:
            return redirect(f"/blog/{blog_id}")
        
@app.route("/new_review/<int:recipe_id>", methods=["POST"])
def new_review(recipe_id):
    require_login()
    
    grade = request.form["grade"]
    review = request.form["review"]
    sql = """INSERT INTO Reviews (reviewer, post, stars, review, time_posted) 
    VALUES (?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [session["id"], recipe_id, grade, review])
    return redirect(f"/recipe/{recipe_id}")

@app.route("/remove_review/<int:review_id>", methods=["POST"])
def remove_review(review_id):
    if "deleterev" in request.form:
        sql = """DELETE FROM Reviews WHERE id = ?"""
        db.execute(sql, [review_id])
    else:
        return abort(403)
    return redirect("/")
        
@app.route("/new_comment/<int:blog_id>", methods=["POST"])
def new_comment(blog_id):
    require_login()

    comment = request.form["comment"]
    sql = """INSERT INTO Comments (commenter, post, comment, time_posted) 
    VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [session["id"], blog_id, comment])
    return redirect(f"/blog/{blog_id}")

@app.route("/remove_comment/<int:comment_id>", methods=["POST"])
def remove_comment(comment_id):
    if "deletecom" in request.form:
        sql = """DELETE FROM Comments WHERE id = ?"""
        db.execute(sql, [comment_id])
    else:
        return abort(403)
    return redirect("/")