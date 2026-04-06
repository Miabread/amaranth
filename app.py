from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Things under /static are served directly without needing anything here
# Every time you make a change to any files being served you gotta restart the webserver too

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

@app.route("/user/<name>")
def welcome(name):
    return render_template("user.html", name=name)

@app.route("/admin/<name>")
def admin_view(name):
    return render_template("admin_view.html", name=name)

def create_inc_id(start=0):
    stored_id = start
    def closure():
        nonlocal stored_id
        id = stored_id
        stored_id += 1
        return id
    return closure

create_post_id = create_inc_id(0)

dummy_post_db = [
    {"post_id": create_post_id(), "title": "Foo title",  "content": "Foo content", "author": "Foo author", "likes": 123 },
    {"post_id": create_post_id(), "title": "Bar title",  "content": "Bar content", "author": "Bar author", "likes": 456 },
    {"post_id": create_post_id(), "title": "Baz title",  "content": "Baz content", "author": "Baz author", "likes": 789 },
    {"post_id": create_post_id(), "title": "Bao title",  "content": "Bao content", "author": "Bao author", "likes": 922 },
    {"post_id": create_post_id(), "title": "Fizz title",  "content": "Fizz content", "author": "Fizz author", "likes": 3 },
    {"post_id": create_post_id(), "title": "Buzz title",  "content": "Buzz content", "author": "Buzz author", "likes": 52 },
    {"post_id": create_post_id(), "title": "Meow title",  "content": "Meow content", "author": "Meow author", "likes": 85 },
    {"post_id": create_post_id(), "title": "Woof title",  "content": "Woof content", "author": "Woof author", "likes": 34 },
]

@app.route("/posts/")
def posts(): 
    return render_template("posts.html", posts = dummy_post_db)

@app.route("/posts/<post_id>")
def posts_id(post_id):
    return render_template("posts_id.html", post = dummy_post_db[int(post_id)])

@app.get("/posts/new")
def posts_new_page():
    return render_template("posts_new.html")

@app.post("/posts/new")
def posts_new_form():
    new_post = { "post_id": create_post_id(), "likes": 0 }
    new_post["title"] = request.form["title"]
    new_post["author"] = request.form["author"]
    new_post["content"] = request.form["content"]
    dummy_post_db.append(new_post)
    return redirect(url_for("posts", posts_id = new_post["post_id"]))

# This whines about "This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
# but that's something to fix in the future. It just requires a different way of starting the sever using some other dependency
if __name__ == '__main__':
    app.run()
