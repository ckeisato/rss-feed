import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.session import Session

app = Flask(__name__)


import db_setup
import views

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'rss_feed.db')
))

