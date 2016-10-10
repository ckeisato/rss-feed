import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from rss_reader import app

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv


def init_db():
  db = get_db()
  with app.open_resource('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
  db.commit()


# init the db
@app.cli.command('initdb')
def initdb_command():
  # Initializes the database.
  init_db()
  print 'Initialized the database.'


# clear the db
@app.cli.command('cleardb')
def cleardb_command():
	db = get_db()
	db.execute('delete from users')
	db.commit()

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