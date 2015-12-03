#!/usr/bin/env python

# all the imports
#from ShareCompute import *
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import datetime

# configuration
DATABASE = '/tmp/Stock.db'
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

#show shares
@app.route('/')
def show_shares():
	today = str(datetime.date.today())
	yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
	cur = g.db.execute('SELECT stock_basics.code, name, c_name, holdingQuantity, close, price_change\
						FROM stock_basics, stock_concept, stock_price \
						WHERE stock_basics.code = stock_concept.code and \
							  stock_concept.code = stock_price.code and \
							  date = ? and \
							  holdingQuantity > 0 \
						ORDER BY stock_basics.code ASC', [yesterday])
	shares = [dict(code=row[0], name=row[1], c_name=row[2], holdingQuantity=row[3],\
				   close=row[4], price_change=row[5]) for row in cur.fetchall()]
	return render_template('show_shares.html', shares = shares, profit = 'Profit(shares)', date = today)

#search_share
@app.route('/search', methods=['GET', 'POST'])
def search_shares():
	yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
	if not request.form['code']:
		return redirect(url_for('show_shares'))
	cur = g.db.execute('SELECT stock_basics.code, name, c_name, holdingQuantity, \
							   close, price_change\
						FROM stock_basics, stock_concept, stock_price \
						WHERE stock_basics.code = stock_concept.code and \
							  stock_concept.code = stock_price.code and \
							  date = ? and\
							  stock_basics.code = ?\
						ORDER BY stock_basics.code ASC', [yesterday, request.form['code']])
	shares = [dict(code=row[0], name=row[1], c_name=row[2], holdingQuantity=row[3],\
				   close=row[4], price_change=row[5]) for row in cur.fetchall()]
	return render_template('search_shares.html', shares = shares)

#modify_share
@app.route('/modify', methods=['POST'])
def modify_share():
	if not session.get('logged_in'):
		abort(401)
	if request.form['code'] and request.form['quantity']:
		g.db.execute('UPDATE stock_basics\
					  SET holdingQuantity = ?\
					  WHERE code = ?', [request.form['quantity'], request.form['code']])
		g.db.commit()
		flash('Share was successfully modified')
	return redirect(url_for('show_shares'))

'''
#del_entry
@app.route('/del', methods=['DELETE'])
def del_share():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('DELETE FROM ENTRIES WHERE ID = {0}'.format(request.form['code'][0]))
	g.db.commit()
	flash('Selected entry was successfully delete')
	return redirect(url_for('show_shares'))
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
			return redirect(url_for('show_shares'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_shares'))


if __name__ == '__main__':
	app.run(host = '0.0.0.0')
