from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'chatassist.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                FOREIGN KEY (user_name) REFERENCES subscribers(name)
            )
        ''')
        db.commit()

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    name = data['name']
    password = data['password']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO subscribers (name, password) VALUES (?, ?)', (name, password))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Subscription successful'}), 201

@app.route('/api/rate', methods=['POST'])
def rate():
    data = request.get_json()
    user_name = data['userName']
    rating_value = data['ratingValue']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ratings (user_name, rating) VALUES (?, ?)', (user_name, rating_value))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Rating submitted'}), 201

@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name, password FROM subscribers')
    subscribers = cursor.fetchall()
    conn.close()
    return jsonify([{'name': name, 'password': password} for name, password in subscribers])

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT user_name, rating FROM ratings')
    ratings = cursor.fetchall()
    conn.close()
    return jsonify([{'name': user_name, 'value': rating} for user_name, rating in ratings])

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
