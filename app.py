from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask(__name__)

url = 'postgres://dpkjxvsf:Hgm0fnTkSKH6auFW7h5WKEYjLgpX_RJn@rogue.db.elephantsql.com/dpkjxvsf'
connection = psycopg2.connect(url)

@app.get('/')
def home():
    return 'Hello, world!'

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
    VALUES (%s, %s, %s, %s, %s, %s);
    """
)

# select empno,ename,hiredate from emp order by hiredate asc;
# asc - ascending (reverse = False)
# desc - descending (reverse = True)

GET_ALL_STUDENTS = (
    """
    SELECT
    first_name, last_name, email, unique_code, registered, year
    from students
    by year %s;
    """
) # %s - asceding or descending

@app.post('/api/student')
def create_user():
    data = request.get_json()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STUDENTS_TABLE)
    
    return "Its ok BRO", 201

@app.get('/api/student')
def get_all_users():
    # args:
    # sorting - True/False
    # reverse - True/False
    # filter - ...
    sorting = request.args.get('sorting')
    reverse = request.args.get('reverse')

    return 'Yeahhh', 201