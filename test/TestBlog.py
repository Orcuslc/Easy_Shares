#!/usr/bin/env python

# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = '/tmp/TestBlog.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create application 
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('TESTBLOG_SETTINGS',silent = True)

#function to connect database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

#initial database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

#connect database
@app.before_request
def before_request():
	g.db = connect_db()

#close database
@app.teardown_request
def teardown_request(exception):
	g.db.close()

#show entries
@app.route('/')
def show_entries():
	cur = g.db.execute('SELECT TITLE, PASSAGE FROM ENTRIES ORDER BY ID DESC')
	entries = [dict(title=row[0], passage=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries = entries)

#add_entry
@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('INSERT INTO ENTRIES (TITLE, PASSAGE) VALUES (?, ?)', [request.form['title'], request.form['passage']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

'''
#del_entry
@app.route('/del', methods=['DELETE'])
def del_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('DELETE FROM ENTRIES WHERE ID = ?', request.form['id'])
	g.db.commit()
	flash('Selected entry was successfully delete')
	return redirect(url_for('show_entries'))

#search_entry
@app.route('/search', methods=['GET'])
def search_entry():
'''	

#login and logout
@app.route('/login',methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))


if __name__ == '__main__':
	app.run(host = '0.0.0.0')

