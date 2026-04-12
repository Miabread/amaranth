from flask import Flask, render_template, request, redirect, url_for, abort, flash
import random
import mysql.connector
from datetime import date
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

app = Flask(__name__)
app.secret_key = "a"

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Things under /static are served directly without needing anything here
# Every time you make a change to any files being served you gotta restart the webserver too

# Change this to be something more secure later, but this is fine and easy for local testing
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="amaranth"
)
cursor = mydb.cursor()

@app.route('/')
def render_base():
    # This works relative to the templates folder by default
    return render_template("home.html")

@app.route('/test-flash')
def test_flash():
    flash("Hello flash", "info")
    return redirect(url_for('signup'))  # page that includes flashing template code


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        pw = request.form.get('password', '')
        pw2 = request.form.get('password2', '')

        if not (username and email and pw and pw2):
            flash("All fields required", "error")
            return redirect('/signup')

        elif len(username) < 3:
            flash("Username must be at least 3 characters", "error")
            return redirect('/signup')

        elif pw != pw2:
            flash("Passwords do not match", "error")
            return redirect('/signup')

        elif len(pw) < 8:
            flash("Password must be at least 8 characters", "error")
            return redirect('/signup')

        hashed = PasswordHasher().hash(pw)

        cursor.execute("SELECT user_id FROM user WHERE username=%s", [username])
        if cursor.fetchone():
            flash("Username is taken", "error")
            return redirect('/signup')

        cursor.execute("SELECT user_id FROM user WHERE email=%s", [email])
        if cursor.fetchone():
            flash("Email already registered", "error")
            return redirect('/signup')

        cursor.execute(
            "INSERT INTO user (type, username, email, password, display_name, date) VALUES (0, %s, %s, %s, %s, NOW())",
            [username, email, hashed, username]
        )
        mydb.commit()
        flash("Account created", "success")
        return redirect('/login')

    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        pw = request.form.get('password', '')

        cursor.execute(
            "SELECT user_id, username, password FROM user WHERE email=%s",
            [email]
        )
        data = cursor.fetchone()
        if not data:
            flash("Email or password is incorrect", "error")
            return redirect('/login')

        try:
            if PasswordHasher().verify(data[2], pw):
                flash("Successfully logged in", "success")
                return redirect(f'/user/{data[1]}')
        except VerifyMismatchError:
            flash("Email or password is incorrect", "error")
            return redirect('/login')
        except Exception as e:
            raise
            flash("An unexpected error has occurred", "error")
            return redirect('/login')

    return render_template("login.html")

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/user/<username>")
def welcome(username):
    # SQL query to select the display name and bio from a user
    query = "SELECT display_name,bio,profile_picture FROM user WHERE username = %s"

    # Execute SQL command using the username to replace %s
    # not sure why the replacement has to be a tuple, but it does
    cursor.execute(query, (username, ))

    # This can be accessed like an array
    dbresult = cursor.fetchone()

    # If cursor.rowcount is 0 then the result doesn't exist'
    if not cursor.rowcount:
        return render_template("notfound.html", type="User", username=username)

    # If there's no profile picture set then change it to use the placeholder one
    profile_picture = dbresult[2]

    # Select everything from all posts and the usernames of those posts
    # If a user doesn't exist it should be NULL
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id WHERE user.username = %s"

    # Execute SQL query
    cursor.execute(query, (username, ))

    # This can be accessed like an array
    posts = cursor.fetchall()
    if not profile_picture:
        profile_picture = "no_profile_picture_set.png"

    return render_template("user.html", username=username, displayname=dbresult[0], bio=dbresult[1], profile_picture=profile_picture, posts=posts)

@app.route("/admin/<name>")
def admin_view(name):
    return render_template("admin_view.html", name=name)

@app.route("/posts/")
def posts():
    # Select everything from all posts and the usernames of those posts
    # If a user doesn't exist it should be NULL
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id"

    # Execute SQL query
    cursor.execute(query)

    # This can be accessed like an array
    dbresult = cursor.fetchall()

    return render_template("posts.html", posts = dbresult)

@app.route("/posts/<post_id>")
def posts_id(post_id):
    # Select everything from the post id and the username who created it
    # If a user doesn't exist it should be NULL
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id WHERE post_id = %s"

    # Execute SQL query
    cursor.execute(query, (post_id, ))

    # This can be accessed like an array
    dbresult = cursor.fetchone()

    return render_template("posts_id.html", post = dbresult)

@app.get("/posts/new")
def posts_new_page():
    return render_template("posts_new.html")

@app.post("/posts/new")
def posts_new_form():
    if "title" not in request.form or 30 < len(request.form["title"]) < 2:
        abort(400, description="Invalid parameter 'title'")

    if "author" not in request.form or 30 < len(request.form["author"]) < 2:
        abort(400, description="Invalid parameter 'author'")

    if "content" not in request.form or 300 < len(request.form["content"]) < 2:
        abort(400, description="Invalid parameter 'content'")

    # Don't need to specify post_id it'll auto increment
    # likes always starts at 0
    query = "INSERT INTO post (title,content,author,date,likes) VALUES (%s,%s,%s,%s,0)"

    # Execute SQL insert
    cursor.execute(query, (request.form["title"], request.form["content"], request.form["author"], date.today()))

    # Actually update the DB
    mydb.commit()

    return redirect("/posts/" + str(cursor.lastrowid))

# This whines about "This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
# but that's something to fix in the future. It just requires a different way of starting the sever using some other dependency
if __name__ == '__main__':
    app.run()
