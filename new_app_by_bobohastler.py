from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/iceland.html")
def iceland():
   return render_template("iceland.html")

@app.route("/main.html")
def main():
   return render_template("main.html")

@app.route("/about.html")
def about():
   return render_template("about.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
   return render_template("register.html", title = "Реєстрація", )

if __name__ == "__main__":
   app.run(debug=True)
