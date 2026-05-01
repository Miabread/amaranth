from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
import random
import mysql.connector
from datetime import date
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './static/profile-pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.secret_key = "a"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

def get_user(username):
    user = {}

    # SQL query to select the display name and bio from a user
    query = "SELECT display_name,bio,profile_picture,email,type,user_id FROM user WHERE username = %s"

    # Execute SQL command using the username to replace %s
    # not sure why the replacement has to be a tuple, but it does
    cursor.execute(query, (username, ))

    # This can be accessed like an array
    dbresult = cursor.fetchone()

    # If cursor.rowcount is 0 then the result doesn't exist'
    if not cursor.rowcount:
        return None

    # If there's no profile picture set then change it to use the placeholder one
    user["profile_picture"] = dbresult[2]

    if not user["profile_picture"]:
        user["profile_picture"] = "no_profile_picture_set.png"

    # Select everything from all posts and the usernames of those posts
    # If a user doesn't exist it should be NULL
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id WHERE user.username = %s"

    # Execute SQL query
    cursor.execute(query, (username, ))

    # This can be accessed like an array
    posts = cursor.fetchall()

    user["display_name"] = dbresult[0]
    user["bio"] = dbresult[1]
    user["email"] = dbresult[3]
    user["posts"] = posts
    user["type"] = dbresult[4]
    user["id"] = dbresult[5]

    return user

def admin():
    # If we aren't signed in then return 0
    if not session.get("username"):
        return 0

    user = get_user(session.get("username"))

    # If we aren't an admin then return 0
    if not user["type"]:
        return 0

    # Otherwise we are an admin, return 1
    return 1

@app.route('/')
def render_base():
    # This works relative to the templates folder by default
    return render_template("home.html")

@app.route("/edit_profile/<username>", methods=['GET', 'POST'])
def edit_profile(username):
    user = get_user(username)

    # If we aren't signed in as the user we're trying to edit then redirect to the homepage
    if not session.get("username") == username:
        return redirect("/")

    if request.method == 'POST':
        display_name = request.form.get('display_name', '').strip() or user['display_name']
        bio = request.form.get('bio', '').strip() or user['bio']
        pfp = request.files['pfp']
        pw = request.form.get('password', '')
        pw2 = request.form.get('password2', '')

        if len(display_name) < 3:
            flash("Display name must be at least 3 characters", "error")
            return redirect(url_for('edit_profile', username=username))

        if pfp.filename != '':
            filename = secure_filename(pfp.filename)
            actual_filename = username + pfp.filename
            pfp.save(os.path.join(app.config['UPLOAD_FOLDER'], actual_filename))
            cursor.execute(
                "UPDATE user SET profile_picture=%s WHERE username=%s",
                (actual_filename, username)
            )

        if pw:
            if pw != pw2:
                flash("Passwords do not match", "error")
                return redirect(url_for('edit_profile', username=username))

            if len(pw) < 8:
                flash("Password must be at least 8 characters", "error")
                return redirect(url_for('edit_profile', username=username))

            hashed = PasswordHasher().hash(pw)

            cursor.execute(
                "UPDATE user SET display_name=%s, bio=%s, password=%s WHERE username=%s",
                (display_name, bio, hashed, username)
            )
        else:
            cursor.execute(
                "UPDATE user SET display_name=%s, bio=%s WHERE username=%s",
                (display_name, bio, username)
            )

        mydb.commit()
        flash("Profile edited", "success")
        return redirect(url_for('edit_profile', username=username))

    return render_template("edit_profile.html", username=username, user=user)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        pw = request.form.get('password', '')
        pw2 = request.form.get('password2', '')

        if not (username and email and pw and pw2):
            flash("All fields required", "error")
            return redirect('/register')

        elif len(username) < 3:
            flash("Username must be at least 3 characters", "error")
            return redirect('/register')

        elif pw != pw2:
            flash("Passwords do not match", "error")
            return redirect('/register')

        elif len(pw) < 8:
            flash("Password must be at least 8 characters", "error")
            return redirect('/register')

        hashed = PasswordHasher().hash(pw)

        cursor.execute("SELECT user_id FROM user WHERE username=%s", [username])
        if cursor.fetchone():
            flash("Username is taken", "error")
            return redirect('/register')

        cursor.execute("SELECT user_id FROM user WHERE email=%s", [email])
        if cursor.fetchone():
            flash("Email already registered", "error")
            return redirect('/register')

        cursor.execute(
            "INSERT INTO user (type, username, email, password, date, display_name, profile_picture, bio, private) VALUES (0, %s, %s, %s, NOW(), %s, 'problem_child.png', '', 0)",
            [username, email, hashed, username]
        )
        mydb.commit()
        flash("Account created", "success")
        return redirect('/login')

    return render_template("register.html")

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
                session["username"] = data[1]
                return redirect("/user/" + data[1])
        except VerifyMismatchError:
            flash("Email or password is incorrect", "error")
            return redirect('/login')
        except Exception as e:
            raise
            flash("An unexpected error has occurred", "error")
            return redirect('/login')

    return render_template("login.html")

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/user/<username>")
def welcome(username):
    user = get_user(username)

    if not user:
        return render_template("notfound.html", type="User", username=username)

    return render_template("user.html", username=username, displayname=user["display_name"], bio=user["bio"], profile_picture=user["profile_picture"], posts=user["posts"])

@app.route("/admin/<name>")
def admin_view(name):
    return render_template("admin_view.html", name=name)

@app.route("/posts/")
def posts():
    # Select everything from all posts and the usernames of those posts
    # If a user doesn't exist it should be NULL
    # Don't show hidden posts
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id WHERE post.hidden = 0"

    # Execute SQL query
    cursor.execute(query)

    # This can be accessed like an array
    dbresult = cursor.fetchall()

    return render_template("posts.html", posts = dbresult)

@app.route("/posts/<post_id>", methods=['GET', 'POST'])
def posts_id(post_id):
    if request.method == 'POST':
        user = get_user(session.get("username"))

        comment = request.form.get('comment', '').strip()
        print(comment)

        cursor.execute(
            "INSERT INTO comment (post_id, content, author, date, likes) VALUES (%s, %s, %s, %s, 0)",
            (post_id, comment, user["id"], date.today())
        )

        mydb.commit()

        return redirect("/posts/" + post_id)

    # Select everything from the post id and the username who created it
    # If a user doesn't exist it should be NULL
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id WHERE post_id = %s"

    # Execute SQL query
    cursor.execute(query, (post_id, ))

    # This can be accessed like an array
    post = cursor.fetchone()

    # If cursor.rowcount is less than 1 then the result doesn't exist (this ended up -1 in testing so we can't just use not)
    if cursor.rowcount < 1:
        return render_template("notfound.html", type="Post", data=post_id)

    # Select all comments on this post
    # If a post doesn't exist it should be NULL
    query = "SELECT comment.*,user.username FROM comment LEFT JOIN user ON comment.author = user.user_id WHERE post_id = %s"

    # Execute SQL query
    cursor.execute(query, (post_id, ))

    # This can be accessed like an array
    comments = cursor.fetchall()

    return render_template("posts_id.html", post = post, comments = comments)

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

@app.route("/admin/posts/")
def admin_posts(): 
    # If we aren't admin then give 403
    if not admin():
        return render_template('denied.html'), 403

    # Select everything from all posts and the usernames of those posts
    # If a user doesn't exist it should be NULL
    # Don't show hidden posts
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id"

    # Execute SQL query
    cursor.execute(query)

    # This can be accessed like an array
    dbresult = cursor.fetchall()

    return render_template("admin_posts.html", posts = dbresult)

@app.route("/admin/posts/<post_id>")
def admin_posts_id(post_id):
    # If we aren't admin then give 403
    if not admin():
        return render_template('denied.html'), 403

    # Select everything from the post id and the username who created it
    # If a user doesn't exist it should be NULL
    query = "SELECT post.*,user.username FROM post LEFT JOIN user ON post.author = user.user_id WHERE post_id = %s"

    # Execute SQL query
    cursor.execute(query, (post_id, ))

    # This can be accessed like an array
    dbresult = cursor.fetchone()

    # If cursor.rowcount is less than 1 then the result doesn't exist (this ended up -1 in testing so we can't just use not)
    if cursor.rowcount < 1:
        return render_template("notfound.html", type="Post", data=post_id)
    
    return render_template("admin_posts_id.html", post = dbresult)

@app.post("/admin/posts/<post_id>/delete")
def admin_posts_id_delete(post_id):
    # If we aren't admin then give 403
    if not admin():
        return render_template('denied.html'), 403

    query = "DELETE FROM post WHERE post_id = %s"

    # Execute SQL delete
    cursor.execute(query, (post_id, ))

    # Actually update the DB
    mydb.commit()

    # Redirect to admin posts
    return redirect(url_for('admin_posts'))

@app.post("/admin/posts/<post_id>/hidden")
def admin_posts_id_hidden(post_id):
    # If we aren't admin then give 403
    if not admin():
        return render_template('denied.html'), 403

    # This inverts the value of hidden, toggling it
    query = "UPDATE post SET hidden = NOT hidden WHERE post_id = %s"

    # Execute SQL delete
    cursor.execute(query, (post_id, ))

    # Actually update the DB
    mydb.commit()

    # Redirect to admin posts
    return redirect(url_for('admin_posts'))

# This whines about "This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
# but that's something to fix in the future. It just requires a different way of starting the sever using some other dependency
if __name__ == '__main__':
    app.run()
