import sqlite3

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

DATABASE = '/SERVER/databases/data_site/data.db'


def create_table():
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS data(Token TEXT UNIQUE  NOT NULL, Data TEXT)')
    db_conn.commit()


@app.route('/new/<token>')
def new_token(token):
    create_table()
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()

    cur.execute(f'''SELECT * FROM data WHERE Token = "{token.replace('"', '""')}"''')

    if not cur.fetchall():
        cur.execute(f'''INSERT INTO data VALUES ("{token.replace('"', '""')}", "")''')
        db_conn.commit()

    return redirect(f'/{token}')


@app.route('/<token>')
def get_data(token):
    create_table()
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()

    cur.execute(f'''SELECT * FROM data WHERE Token = "{token.replace('"', '""')}"''')
    f = cur.fetchall()
    if not f:
        return redirect(f'/new/{token}')
    data = f[0][1]

    return render_template('data.html', data=data, token=token)


@app.route('/send-data')
def send_data():
    token = request.args['token']
    data = request.args['data']
    print(f'GOT  token = "{token}", data = "{data}"')

    create_table()
    db_conn = sqlite3.connect(DATABASE)
    cur = db_conn.cursor()

    cur.execute(f'''UPDATE data SET Data = "{data.replace('"', '""')}" WHERE Token = "{token.replace('"', '""')}"''')
    db_conn.commit()

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
