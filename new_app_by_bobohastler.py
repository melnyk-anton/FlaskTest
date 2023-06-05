from flask import Flask, render_template, url_for, request, flash
import psycopg2
from random import randint

app = Flask(__name__)
app.config["SECRET_KEY"] = "hui"

url = 'postgres://dpkjxvsf:Hgm0fnTkSKH6auFW7h5WKEYjLgpX_RJn@rogue.db.elephantsql.com/dpkjxvsf'
connection = psycopg2.connect(url)

CREATE_STUDENTS_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS students (
    id serial PRIMARY KEY NOT NULL, 
    first_name VARCHAR ( 30 ) NOT NULL,
    last_name VARCHAR ( 30 ) NOT NULL,
    email VARCHAR ( 30 ) UNIQUE NOT NULL,
    unique_code VARCHAR ( 10 ) UNIQUE NOT NULL,
    registered TIMESTAMP,
    year INT NOT NULL
    );
    """
)

INSERT_STUDENT = (
    """
    INSERT INTO students (
        first_name,
        last_name,
        email,
        unique_code,
        registered,
        year
    )
    VALUES (%s, %s, %s, %s, now() at time zone 'EETDST', %s);
    """
)

@app.route("/iceland.html")
def iceland():
    return render_template("iceland.html")

@app.route("/main.html")
def main():
    return render_template("main.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

def generate_unique_code():
    len_ = 10
    s = ''
    for i in range(len_):
        s += str(randint(0, 9))
    return s

@app.route("/register.html", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        first_name = request.form["name"]
        last_name = request.form["surname"]
        year = request.form["year"]
        if len(email) >= 10:
            flash("Дякую за реєстрацію !")
        else:
            flash("Помилка реєстрації")

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_STUDENTS_TABLE)
                cursor.execute(INSERT_STUDENT, (first_name, last_name, email, generate_unique_code(), year)) # without current_time
    
    return render_template("register.html", title = "Реєстрація", )

if __name__ == "__main__":
    app.run(debug=True)
