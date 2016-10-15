import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.session import Session

app = Flask(__name__)


import rss_db
import views

app.secret_key = os.urandom(24)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'rss_feed.db')
))

