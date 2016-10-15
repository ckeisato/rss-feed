from rss_reader import app
from flask import render_template, session, request, redirect, flash, url_for
from flask.ext.session import Session

import rss_db
import pdb

Session(app)

# ROUTES
@app.route('/')
def index_page():
  users = rss_db.get_users()
  return render_template('show_users.html', users=users)

@app.route('/new-user', methods=['GET', 'POST'])
def new_user():
	return render_template('create_user.html')

@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
  rss_db.create_user(request.form['username'], request.form['password'])
  return redirect(url_for('index_page'))


@app.route('/add_feed', methods=['GET', 'POST'])
def add_feed():
  if request.method == 'POST':
    feed = request.form['new-feed-entry']
    rss_db.add_feed(feed, session['user-id'])
  return redirect(url_for('profile'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
  username = rss_db.get_loggedin_user(session['user-id'])
  feeds = rss_db.get_loggedin_feeds(session['user-id'])
  return render_template('profile.html', username=username, feedArray=feeds)

@app.route('/feeds', methods=['GET', 'POST'])
def feeds():
  username = rss_db.get_loggedin_user(session['user-id'])
  feeds = rss_db.get_loggedin_feeds(session['user-id'])
  return render_template('feeds.html', username=username, feedArray=feeds)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    user_id = rss_db.get_user_id(request.form['username'], request.form['password'])
    # pdb.set_traces()
    if user_id is not None:
      session['user-id'] = user_id
      return redirect(url_for('profile'))
    else:
      return redirect(url_for('new_user'))
  return render_template('login.html')


@app.route('/logout')
def logout():
    session['user-id'] = 0
    return redirect(url_for('index_page'))


@app.route('/is_logged_in')
def is_logged_in():
  if 'user-id' in session:
    return True
  return False


@app.route('/getsession')
def getsession():
  if 'user-id' in session:
    return session['user-id']
  else:
    return 'not logged in'

@app.route('/dropsession')
def dropsession():
  session.pop('user-id', None)
  return 'dropped'
