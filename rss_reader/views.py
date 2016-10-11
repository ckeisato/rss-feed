from rss_reader import app
from flask import render_template, session, request, redirect, flash, url_for
from flask.ext.session import Session

import db_setup
import pdb

Session(app)

# ROUTES
@app.route('/')
def index_page():
  db = db_setup.get_db()
  cur = db.execute('select username, password from users order by id desc')
  users = cur.fetchall()
  return render_template('show_users.html', users=users)

@app.route('/new-user', methods=['GET', 'POST'])
def new_user():
	return render_template('create_user.html')

@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
	db= db_setup.get_db()
	db.execute('insert into users (username, password) values (?, ?)',[request.form['username'], request.form['password']])
	db.commit()
	return redirect(url_for('index_page'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
  db = db_setup.get_db()
  username = db.execute("select username from users where id =" + session['user-id']).fetchone()[0]
  feed = db.execute("select feeds from users where id =" + session['user-id']).fetchone()[0]
  return render_template('profile.html', username=username, feed=feed)

@app.route('/login', methods=['GET', 'POST'])
def login():
  db = db_setup.get_db()
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user_id = db.execute("select id from users where username = " + username + " and password = " + password)

    if user_id != None:
      session['user-id'] = str(user_id.fetchone()[0])
      return redirect(url_for('profile'))
    else:
      return redirect(url_for('create-user'))
  return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    

