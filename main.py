import uuid
import time
from flask import Flask, request
import sqlite3
import json
app = Flask(__name__)


def initDb():
    db = sqlite3.connect('log.sqlite')
    cur = db.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS items (
                uuid VARCHAR(80) PRIMARY KEY,
                timestamp INTEGER NOT NULL,
                method VARCHAR(20) NOT NULL,
                get TEXT,
                post TEXT,
                headers TEXT
            )
    ''')
    return db
initDb()

@app.route('/', defaults={'path': '/'}, methods=['POST','GET'])
@app.route('/<path:path>', methods=['POST','GET'])
def log_me(path):
    db = sqlite3.connect('log.sqlite')
    an_id = uuid.uuid4().hex
    a_time = int(time.time())
    if request.method == 'POST':
        postdata = json.dumps(str(request.data), indent=4)
    else:
        postdata = None
    headers = json.dumps(dict(request.headers), indent=4)

    cur = db.cursor()
    cur.execute('''
            INSERT INTO items(uuid,timestamp,method,get,post,headers) VALUES (?,?,?,?,?,?)''',
            [an_id, a_time, request.method, path, postdata, headers])
    db.commit()
    return 'OK'

app.secretkey = '6c5a05d7acd43743adeb48a1ce74a385'
app.debug = False

if __name__ == '__main__':
    app.run()

