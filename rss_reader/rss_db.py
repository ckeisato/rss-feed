import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.session import Session

from rss_reader import app
import pdb

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv

def init_db():
  db = get_db()
  with app.open_resource('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
  db.commit()

def get_db():
  # Opens a new database connection if there is none yet for the current application context.
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

def get_users():
  db = get_db()
  users = db.execute('select username, password from users order by id desc').fetchall()
  return users

def get_loggedin_user(_id):
  db = get_db()
  return db.execute("select username from users where id =" + _id).fetchone()[0]


def get_loggedin_feeds(_id):
  db = get_db()
  feeds = db.execute("select feeds from users where id =" + _id).fetchone()
  if feeds is None:
    return None
  else: 
    return feeds[0].split(",")

def get_user_id(username, password):
  db = get_db()
  user_id = db.execute("select id from users where username = '" + username + "' and password = '" + password + "'").fetchone()
  if user_id is None:
    return None
  else:
    return str(user_id[0])

def create_user(username, password):
  db = get_db()
  db.execute('insert into users (username, password, feeds) values (?, ?, ?)',[username, password, ''])
  db.commit()

def add_feed(feed, id):
  db = get_db()
  db.execute("update users set feeds = '" + feed + "," + "' || feeds where id=" + session['user-id'])  
  db.commit()

# init the db
@app.cli.command('initdb')
def initdb_command():
  init_db()
  print 'Initialized the database.'

# clear the db
@app.cli.command('cleardb')
def cleardb_command():
	db = get_db()
	db.execute('delete from users')
	db.commit()

@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()

