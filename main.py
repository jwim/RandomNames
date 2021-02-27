from flask import Flask, render_template
import sqlite3
from sqlite3 import Error
import requests
import json

app = Flask(__name__)


database = sqlite3.connect('database.db')
# database.execute("CREATE TABLE names (first TEXT, last TEXT)")


@app.route('/')
def home():
    response = requests.get("https://randomuser.me/api/?results=1000&inc=name")
    num = 0

    if response.status_code != 200:
        # This means something went wrong.
        print("Incorrect API")
        pass
    else:
        data = json.loads(response.text)
        with sqlite3.connect("database.db") as db:
            for random_n in data['results']:
                fname = random_n['name']['first']
                lname = random_n['name']['last']

                current_cursor = db.cursor()
                current_cursor.execute("INSERT INTO names (first, last) VALUES (?, ?)", (fname, lname))
                db.commit()
                num += 1
    return "Okay"

@app.route('/list')
def list():
    db = sqlite3.connect("database.db")
    db.row_factory = lambda cursor, row: row[0]
    cursor = db.cursor()
    names = cursor.execute("SELECT first FROM names").fetchmany(100)

    return render_template("names.html")

if __name__ == '__main__':


    app.run()
