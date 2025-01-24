from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request

app = Flask(__name__)

class Database:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.metadata = MetaData(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def fetch_all(self, table_name):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.engine.connect() as conn:
            result = conn.execute(table.select()).fetchall()
        return [dict(row) for row in result]

    def filter_data(self, table_name, column, value):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.engine.connect() as conn:
            query = table.select().where(table.c[column] == value)
            result = conn.execute(query).fetchall()
        return [dict(row) for row in result]

# Database configuration
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/NaturalDisaster"
db = Database(DATABASE_URL)

@app.route('/data/<table_name>', methods=['GET'])
def get_data(table_name):
    try:
        data = db.fetch_all(table_name)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/filter/<table_name>', methods=['GET'])
def filter_data(table_name):
    column = request.args.get('column')
    value = request.args.get('value')
    if not column or not value:
        return jsonify({'error': 'Missing value parameter'}), 400

    try:
        data = db.filter_data(table_name, column, value)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)