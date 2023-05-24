from flask import Flask, render_template

app = Flask(__name__)

@app.route("/about")
@app.route("/")
def index():
    return render_template('aboutr2d2.html')

@app.route("/about")
def about():
    return "ABOUT"

if __name__ == "__main__":
    app.run(debug=True)
