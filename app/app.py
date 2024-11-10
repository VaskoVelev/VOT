from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )

def index():
    connection = get_db_connection()

    cursor = connection.cursor()
    cursor.execute("select * from mytable;")

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(items)

if __name__ == '__main__':
    app.run(host='0.0.0.0')