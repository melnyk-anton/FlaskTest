from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> Я НЕ БУДУ ЗАЙМАТИСЬ HTML </h1>"

@app.route("/about")
def about():
    return "ABOUT"

if __name__ == "__main__":
    app.run(debug=True)
