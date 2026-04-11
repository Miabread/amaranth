from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/user/<name>")
def welcome(name):
    return render_template("user.html", name=name)

@app.route("/admin/<name>")
def admin_view(name):
    return render_template("admin_view.html", name=name)



# This whines about "This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
# but that's something to fix in the future. It just requires a different way of starting the sever using some other dependency
if __name__ == '__main__':
    app.run()
