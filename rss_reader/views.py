from rss_reader import app

# ROUTES
@app.route('/')
def index_page():
  db = app.get_db()
  return "hello world"

  # db = get_db()
#   cur = db.execute('select username, password from users order by id desc')
#   users = cur.fetchall()
#   return render_template('show_users.html', users=users)


# @app.route('/new-user', methods=['GET', 'POST'])
# def new_user():
# 	return render_template('create_user.html')

# @app.route('/create-user', methods=['GET', 'POST'])
# def create_user():
# 	db = get_db()
# 	db.execute('insert into users (username, password) values (?, ?)',[request.form['username'], request.form['password']])
# 	db.commit()
# 	return redirect(url_for('index_page'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#   error = None
#   if request.method == 'POST':
#     if request.form['username'] != app.config['USERNAME']:
#       error = 'Invalid username'
#     elif request.form['password'] != app.config['PASSWORD']:
#       error = 'Invalid password'
#     else:
#       session['logged_in'] = True
#       flash('You were logged in')
#       return redirect(url_for('show_entries'))
#   return render_template('login.html', error=error)


# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))
    

