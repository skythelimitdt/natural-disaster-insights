from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="my_project_db",
        user="your_username",
        password="your_password",
        host="localhost"
    )

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route('/sales', methods=['GET'])
def get_sales():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales;")
    sales = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(sales)

if __name__ == '__main__':
    app.run(debug=True)