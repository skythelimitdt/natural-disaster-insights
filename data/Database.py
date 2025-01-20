from flask import Flask, jsonify, request
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Database configuration
DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Load table metadata
table1 = Table('one', metadata, autoload_with=engine)
table2 = Table('two', metadata, autoload_with=engine)

@app.route('/users', methods=['GET'])
def get_table1():
    with engine.connect() as conn:
        result = conn.execute(table1.select()).fetchall()
    return jsonify([dict(row) for row in result])

@app.route('/users', methods=['GET'])
def get_table2():
    with engine.connect() as conn:
        result = conn.execute(table2.select()).fetchall()
    return jsonify([dict(row) for row in result])

if __name__ == '__main__':
    app.run(debug=True)