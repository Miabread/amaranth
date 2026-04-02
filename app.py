from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

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

@app.route("/signup")
def signin():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user/<username>")
def welcome(username):
    # SQL query to select the display name and bio from a user
    query = "SELECT display_name,bio,profile_picture FROM user WHERE username = %s"

    # Execute SQL command using the username to replace %s
    # not sure why the replacement has to be a tuple, but it does
    cursor.execute(query, (username, ))

    # This can be accessed like an array
    dbresult = cursor.fetchone()

    # If there's no profile picture set then change it to use the placeholder one
    profile_picture = dbresult[2]
    if not profile_picture:
        profile_picture = "no_profile_picture_set.png"

    # If cursor.rowcount is 0 then the result doesn't exist'
    if not cursor.rowcount:
        return render_template("notfound.html", type="User", username=username)
    else:
        return render_template("user.html", username=username, displayname=dbresult[0], bio=dbresult[1], profile_picture=profile_picture)

@app.route("/admin/<name>")
def admin_view(name):
    return render_template("admin_view.html", name=name)

dummy_post_db = [
    {"post_id": 0, "title": "Foo title",  "content": "Foo content", "author": "Foo author", "likes": 123 },
    {"post_id": 1, "title": "Bar title",  "content": "Bar content", "author": "Bar author", "likes": 456 },
    {"post_id": 2, "title": "Baz title",  "content": "Baz content", "author": "Baz author", "likes": 789 },
    {"post_id": 3, "title": "Bao title",  "content": "Bao content", "author": "Bao author", "likes": 922 },
    {"post_id": 4, "title": "Fizz title",  "content": "Fizz content", "author": "Fizz author", "likes": 3 },
    {"post_id": 5, "title": "Buzz title",  "content": "Buzz content", "author": "Buzz author", "likes": 52 },
    {"post_id": 6, "title": "Meow title",  "content": "Meow content", "author": "Meow author", "likes": 85 },
    {"post_id": 7, "title": "Woof title",  "content": "Woof content", "author": "Woof author", "likes": 34 },
]

@app.route("/posts/")
def posts(): 
    return render_template("posts.html", posts = dummy_post_db)

@app.route("/posts/<post_id>")
def posts_id(post_id):
    return render_template("posts_id.html", post = dummy_post_db[int(post_id)])

# This whines about "This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
# but that's something to fix in the future. It just requires a different way of starting the sever using some other dependency
if __name__ == '__main__':
    app.run()
