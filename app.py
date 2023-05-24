from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
from random import randint
import json

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

@app.post('/api/student')
def create_user():
    data = request.get_json()
    # SELECT now() AT TIME ZONE 'Europe/Paris';
    # timezone - 'EETDST'
    if not ('first_name' in data and 'last_name' in data and 'email' in data and 'year' in data):
        return 'Request should contain at least 4 arguments:\n"first_name" ; "last_name" ; "email" ; "year"', 400

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STUDENTS_TABLE)
            cursor.execute(INSERT_STUDENT, (data['first_name'], data['last_name'], data['email'], generate_unique_code(), data['year'])) # without current_time
    
    return "Its ok BRO", 201

def generate_unique_code():
    len_ = 10
    s = ''
    for i in range(len_):
        s += str(randint(0, 9))
    
    return s

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