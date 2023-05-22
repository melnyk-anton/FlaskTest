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
    """CREATE TABLE IF NOT EXISTS students (
        id serial PRIMARY KEY NOT NULL, 
        first_name VARCHAR ( 30 ) NOT NULL,
        last_name VARCHAR ( 30 ) NOT NULL,
        email VARCHAR ( 30 ) UNIQUE NOT NULL,
        unique_code VARCHAR ( 10 ) UNIQUE NOT NULL,
        registered TIMESTAMP,
        year INT NOT NULL
    );"""
)

@app.post('/api/student')
def create_user():
    data = request.get_json()
    first_name = data['first_name']
    print(first_name)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STUDENTS_TABLE)
            # cursor.execute()
    
    return "Its ok BRO", 201