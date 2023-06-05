from flask import Flask, render_template, url_for, request, flash, jsonify
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

# asc - ascending (reverse = False)
# desc - descending (reverse = True)

GET_ALL_STUDENTS = (
    """
    SELECT
    first_name, last_name, email, unique_code, registered, year
    from students
    %s
    %s;
    """
)
# first %s - where year = x
# second %s - 'order by year' + asceding or descending

GET_STUDENT_BY_ID = (
    """
    SELECT * from students where id = %s;
    """
)

CHANGE_STUDENT_BY_ID = (
    """
    UPDATE students
    SET
    first_name = %s,
    last_name = %s,
    email = %s,
    year = %s
    WHERE id=%s;
    """
)

DELETE_STUDENT_BY_ID = (
    """
    DELETE FROM students
    WHERE id = %s;
    """
)

@app.route("/iceland")
def iceland():
    return render_template("iceland.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/about")
def about():
    return render_template("about.html")

def generate_unique_code():
    len_ = 10
    s = ''
    for i in range(len_):
        s += str(randint(0, 9))
    return s

@app.route("/api/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        first_name = request.form["name"]
        last_name = request.form["surname"]
        year = request.form["year"]
        if len(email) >= 10:
            flash("Дякую за реєстрацію !")

            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_STUDENTS_TABLE)
                    cursor.execute(INSERT_STUDENT, (first_name, last_name, email, generate_unique_code(), year)) # without current_time
        else:
            flash("Помилка реєстрації")
    
    return render_template("register.html", title = "Реєстрація", )

@app.get('/api/student')
def get_all_users():
    # args:
    # sorting (maybe 'sort' is better) - asc/desc
    # filter - int

    sorting = request.args.get('sorting')
    filter_ = request.args.get('filter')


    if sorting != None and not sorting.lower() in ['asc', 'desc']:
        return 'Sorting argument should be "asc" or "desc"', 400
    if sorting != None:
        sorting = f'order by year {sorting}'

    
    if filter_ == None:
        filter_ = ''
    else:
        try:
            filter_ = int(filter_)
        except:
            return 'Type of filter should be Integer type', 400
        
        filter_ = f'where year = {filter_}' 

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_STUDENTS % (filter_, sorting, ))
            t = cursor.fetchall()

            return t, 201

@app.get('/api/student/<id>')
def get_user_by_id(id):
    try:
        id = int(id)
    except:
        return 'Bad ID, should be int', 400
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_STUDENT_BY_ID % id)
            return jsonify(cursor.fetchone()), 201

if __name__ == "__main__":
    app.run(debug=True)
