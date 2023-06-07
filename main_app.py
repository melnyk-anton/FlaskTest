from flask import Flask, render_template, url_for, request, jsonify, flash
import psycopg2
from random import randint

url = "postgres://ayjyxmhl:zCwVAu_nXcqxqGaa2IcZ3_sqMuX92f4a@rogue.db.elephantsql.com/ayjyxmhl"
connection = psycopg2.connect(url) #підключаюсь до бд
connection.autocommit = True #автоматично буде виконувати запроси коли потрібно

app = Flask(__name__) #створюю програму
app.config['SECRET_KEY'] = 'njkdvnsdjvnsdjkvsd' #секретний ключ

def generate_unique_code(): #генерує унікальний код
    len_ = 10
    s = ''
    for i in range(len_):
        s += str(randint(0, 9))
    
    return s

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

with connection.cursor() as cursor: #створюю таблицю
    cursor.execute
    (
        CREATE_STUDENTS_TABLE
    )

@app.route("/api/register", methods = ["POST", "GET"]) #сторінка з текстовими полями для реєстрації
def register():
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
            flash("Ви успішно зареєстровані !")
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_STUDENTS_TABLE)
                    cursor.execute(INSERT_STUDENT, (first_name, last_name, email, generate_unique_code(), year))
                    print("Дані успішно додано до таблиці")

    return render_template("register.html")

@app.route("/api/change/<int:id>", methods = ["POST", "GET"]) #сторіна для зміни даних в таблиці
def change(id):
    id = str(id)
    with connection: #ввожу дані в текстове поле
        with connection.cursor() as cursor:
            cursor.execute(GET_STUDENT_BY_ID, (id))
            l = cursor.fetchone()
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

if __name__ == "__main__":
    app.run(debug=True)