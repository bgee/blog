import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override that from environment variable
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flaskr.db'),
                   DEBUG=True,
                   SECRET_KEY='development key',
                   USERNAME='admin',
                   PASSWORD='default'
                   ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open.resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/add_comment', methods=['POST'])
def add_comment():
    db = get_db()
    db.execute('insert into comments (commenter, text) values (?, ?)',
               [request.form['commenter'], request.form['text']])
    db.commit()
    flash('New comment was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/post/<title>')
def show_post(title):
    db = get_db()
    cur = db.execute('select title, text from entries where title=(?) order by id desc', [title])
    entries = cur.fetchall()
    return render_template('show_posts.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None) # trick
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()