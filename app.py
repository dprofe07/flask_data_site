import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for


if os.path.exists('/SERVER/is_server'):
    prefix = '/info-storage'
    DATABASE = '/SERVER/databases/data_site/data.db'
else:
    prefix = ''
    DATABASE = 'data.db'


app = Flask(__name__, f'{prefix}/static')


def create_table():
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS data(Token TEXT UNIQUE  NOT NULL, Data TEXT)')
    db_conn.commit()


@app.route(f'{prefix}/')
def index():
    return render_template('index.html')


@app.route(f'{prefix}/new/<token>')
def new_token(token):
    create_table()
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()

    cur.execute(f'''SELECT * FROM data WHERE Token = "{token.replace('"', '""')}"''')

    if not cur.fetchall():
        cur.execute(f'''INSERT INTO data VALUES ("{token.replace('"', '""')}", "")''')
        db_conn.commit()

    return redirect(url_for('get_data', token=token))


@app.route(f'{prefix}/<token>')
def get_data(token):
    create_table()
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()

    cur.execute(f'''SELECT * FROM data WHERE Token = "{token.replace('"', '""')}"''')
    f = cur.fetchall()
    if not f:
        return redirect(f'/new/{token}')
    data = f[0][1]

    return render_template('data.html', data=data.replace('!!!newline!!!', '\n'), token=token)


@app.route(f'{prefix}/send-data')
def send_data():
    token = request.args['token']
    data = request.args['data']
    print(f'GOT token = "{token}", data = "{data}"')

    create_table()
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()

    cur.execute(f'''UPDATE data SET Data = "{data.replace('"', '""')}" WHERE Token = "{token.replace('"', '""')}"''')
    db_conn.commit()

    return redirect(url_for('get_data', token=token))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
