import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'rss_feed.db'),
	SECRET_KEY='development_key',
	USERNAME='admin',
	PASSWORD='default'
))

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv


def init_db():
  db = get_db()
  with app.open_resource('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
  db.commit()


@app.cli.command('initdb')
def initdb_command():
  # Initializes the database.
  init_db()
  print 'Initialized the database.'


def get_db():
  # Opens a new database connection if there is none yet for the current application context.
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
  # Closes the database again at the end of the request.
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()


# ROUTES
@app.route('/')
def indexPage():
  db = get_db()
  cur = db.execute('select username, password from users order by id desc')
  users = cur.fetchall()
  return render_template('show_users.html', users=users)


if __name__ == '__main__':
  app.run()
