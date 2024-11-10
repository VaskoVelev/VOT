from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'db'),
        database=os.getenv('DATABASE_NAME', 'vot_web_app'),
        user=os.getenv('DATABASE_USER', 'vasko'),
        password=os.getenv('DATABASE_PASSWORD', 'vasko_123')
    )

def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mytable (
            person_id SERIAL PRIMARY KEY,
            name TEXT,
            height TEXT,
            age INTEGER
        );
    """)

    cursor.execute("""
        INSERT INTO mytable (name, height, age)
        SELECT 'Vasil', '184', 17
        WHERE NOT EXISTS (SELECT 1 FROM mytable WHERE name = 'Vasil');

        INSERT INTO mytable (name, height, age)
        SELECT 'Georgi', '180', 21
        WHERE NOT EXISTS (SELECT 1 FROM mytable WHERE name = 'Georgi');

        INSERT INTO mytable (name, height, age)
        SELECT 'Ivan', '177', 15
        WHERE NOT EXISTS (SELECT 1 FROM mytable WHERE name = 'Ivan');
    """)

    connection.commit()
    cursor.close()
    connection.close()

@app.route('/')
def index():
    create_table()

    connection = get_db_connection()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM mytable;")

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)