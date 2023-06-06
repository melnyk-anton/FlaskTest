from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/register")
def change():
    return render_template("register.html", title = "Register")


if __name__ == "__main__":
    app.run(debug=True)