from flask import Flask, render_template, send_file, request, flash, jsonify
import psycopg2
from random import randint
import os
import pandas as pd

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.config["SECRET_KEY"] = "hui"

url = 'postgres://ayjyxmhl:zCwVAu_nXcqxqGaa2IcZ3_sqMuX92f4a@rogue.db.elephantsql.com/ayjyxmhl' #бодіна бд
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

CHECK_EMAIL_FOR_UNIQUE = (
    """
    %s in (SELECT email FROM students)
    """
)


@app.route("/api/excel", methods = ["POST", "GET"])
def excel():
    if request.method == "POST":
        if 'excel' in request.files:
            errors = []
            file = request.files['excel']

            data = pd.read_excel(file)

            column_names = list(data.columns)

            # Завантажувати потрібно заповнений шаблон екселя, тому перевіряємо як мінімум чи рівні назви колонок з шаблоном.
            if column_names != ['first_name', 'last_name', 'email', 'year']:
                flash('its bad bro, excel file should be in correct format (download example)')

                return render_template('excel.html')
            
            for i in range(len(data.index)):
                first_name, last_name, email, year = data.iloc[i]

                if True in list(data.iloc[i].isnull()):
                    errors.append(['all values should not be null', [first_name, last_name, email, year]])
                    continue

                try:
                    year = int(year)
                except:
                    errors.append(['year should be int', [first_name, last_name, email, year]])
                    continue

                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(CREATE_STUDENTS_TABLE)
                        try:
                            cursor.execute(INSERT_STUDENT, (first_name, last_name, email, generate_unique_code(), year))
                        except:
                            errors.append(['email should be unique', [first_name, last_name, email, year]])

            if errors == []:
                flash('all good bro')
            else:
                flash(f'occured {len(errors)} errors:\n{errors}')
        else:
            flash('its bad bro, you should upload a file')

    return render_template("excel.html")

@app.route("/api/delete", methods = ["POST", "GET"])
def delete():
    if request.method == "POST":
        id = request.form["id"]
        try:
            id = int(id)
        except:
            flash("Треба, щоб id був int")
        finally:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_STUDENT_BY_ID % id)
                    flash("vso harasho")
    return render_template("delete.html")


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

@app.get('/api/student/all')
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

@app.route('/api/student/<int:id>', methods = ["POST", "GET"])
def get_user_by_id(id):
    try:
        id = int(id)
    except:
        return 'Bad ID, should be int', 400
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_STUDENT_BY_ID % id)
            return jsonify(cursor.fetchone()), 201
        
@app.route("/api/student/<int:id>/edit", methods = ["POST", "GET"]) #сторінка для зміни даних в таблиці
def update(id):
    id = str(id)
    with connection: #ввожу дані в текстове поле
        with connection.cursor() as cursor:
            cursor.execute(GET_STUDENT_BY_ID, (id))
            l = cursor.fetchone()

            if l == None:
                return 'Student with this ID does not exist'
            
            first_name = l[1]
            last_name = l[2]
            email = l[3]
            year = l[6]

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        year = request.form['year']
        year = int(year)

        op = True #булова змінна, яка перевіряє, чи все впорядку
        if (len(first_name) > 30):
            flash("Ім'я повинно бути довжиною менше 30 символів")
            op = False
        if (len(last_name) > 30):
            flash("Прізвище повинно бути довжиною менше 30 символів")
            op = False
        if (len(email) > 30):
            flash("Пошта повинна бути довжиною менше 30 символів")
            op = False
        
        if op:
            flash("Дані успішно змінено !")
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_STUDENTS_TABLE)
                    cursor.execute(CHANGE_STUDENT_BY_ID, (first_name, last_name, email, year, id))
                    print("Дані успішно змінено")
    
    return render_template("change.html", first_name = first_name, last_name = last_name, email = email, year = year, action = "/api/change/"+id)

@app.errorhandler(404)
def error(error):
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
