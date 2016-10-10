import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

import db_setup
import views

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'rss_feed.db'),
	SECRET_KEY='development_key',
	USERNAME='admin',
	PASSWORD='default'
))




# @app.route('/profile/<username>')
# def profile(username):


