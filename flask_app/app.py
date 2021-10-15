import os.path
from flask import Flask, render_template, jsonify, request, redirect, url_for

from scraper import scraper
from threading import Thread
import sqlite3 as sql


app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "codal_dps.db")


def db_connection():
    conn = None
    try:
        conn = sql.connect(db_path)
    except sql.Error as e:
        print(e)
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Enter json data:

        # data = request.json
        # symbol = data.get('symbol')

        # Enter form data:
        symbol = request.form['symbol']

        sql_query = f"SELECT * FROM dps_table WHERE name='{symbol}'"
        conn = db_connection()
        cursor = conn.execute(sql_query)
        dps_list = [dict(name=row[0], dps=row[1], date=row[2])
                    for row in cursor.fetchall()]

        if dps_list:
            return jsonify(dps_list)
        else:
            error_message = {
                'error message': 'نام نماد را درست وارد کنید',
            }
            return jsonify(error_message)
    else:
        return render_template("index.html")

# Thread(target=scraper).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
