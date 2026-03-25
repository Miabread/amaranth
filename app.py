from flask import Flask, render_template

app = Flask(__name__)

# Things under /static are served directly without needing anything here

@app.route('/')
def render_base():
    # This works relative to the templates folder by default
    return render_template("extend.html")

@app.route("/<name>")
def welcome(name):
    return render_template("extend.html", name=name)

# This whines about "This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
# but that's something to fix in the future. It just requires a different way of starting the sever using some other dependency
if __name__ == '__main__':
    app.run()
