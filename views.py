﻿"""
Routes and views for the flask application.
"""

from datetime import datetime
from __init__ import app
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import flask
from ShareCompute import Profit

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'personal_info.html',
        today = datetime.now().date(),
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/download/<path:filename>')
def download_file(filename):
	return flask.send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/easyshares')
def easyshares():
	return render_template('index.html', today = datetime.now().date(),
										title = 'Easy Shares',
										year = datetime.now().year)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact Me if there are further questions' ,
        year=datetime.now().year,
    )

@app.route('/Projects')
def Projects():
    """Renders the projects page."""
    cur = g.db.execute('select title, url, text from projects')
    projects = [dict(title=row[0], url=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template(
        'projects.html',
        title='Other Projects',
        year=datetime.now().year,
        projects = projects
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('easyshares'))
    return render_template(
        'login.html',
        title = 'Login',
        year = datetime.now().year,
        error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('home'))

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
@app.route('/show_shares')
def show_shares():
	today = datetime.now().date
	cur = g.db.execute('SELECT DISTINCT X.code, name,\
							   date, holdingQuantity, close, price_change\
						FROM (SELECT code, name, holdingQuantity\
						 	  FROM stock_basics\
						 	  WHERE holdingQuantity > 0) AS X,\
							 (SELECT code, date, close, price_change\
                        	  FROM  (SELECT code, date, close, price_change FROM stock_price) AS Y\
							  WHERE date in (SELECT MAX(date) \
							  				 FROM (SELECT code, date FROM stock_price) AS Z\
							  				 WHERE Z.code = Y.code)) AS W\
						WHERE X.code = W.code \
						ORDER BY X.code ASC')
	shares = [dict(code=row[0], name=row[1], date=row[2], holdingQuantity=row[3],\
				   close=row[4], price_change=row[5]) for row in cur.fetchall()]
	return render_template('show_shares.html', title = 'Show Shares', shares = shares, profit = Profit(shares), date = today, year = datetime.now().year)

#redirect to share information
@app.route('/search_shares', methods=['GET', 'POST'])
def search_shares():
	if not request.form['code']: return redirect(url_for('show_shares'))
	return redirect(url_for('share_inform', code=request.form['code']))

#search_share
@app.route('/<code>', methods=['GET', 'POST'])
def share_inform(code):
	cur = g.db.execute('SELECT DISTINCT X.code, name,\
							    		c_name,\
							    		holdingQuantity, close, price_change, date\
						FROM (SELECT code, holdingQuantity, name FROM stock_basics WHERE code = ?) AS X, \
							 (SELECT code, c_name FROM stock_concept WHERE code = ?) AS Y,\
							 (SELECT code, date, close, price_change\
							  FROM  (SELECT code, date, close, price_change FROM stock_price WHERE code = ?) AS Z\
							  WHERE date in (SELECT MAX(date) \
							  				 FROM (SELECT code, date FROM stock_price) AS W\
							  				 WHERE W.code = ?)) AS V\
						WHERE X.code = Y.code and\
							  Y.code = V.code\
						ORDER BY X.code ASC', [code for i in range(4)])
	shares = [dict(code=row[0], name=row[1], c_name=row[2], holdingQuantity=row[3],\
				   close=row[4], price_change=row[5], date=row[6]) for row in cur.fetchall()]
	length = len(shares)
	return render_template(
        'search_shares.html', 
        title = 'Search',
        shares = shares,
        len = length,
        year = datetime.now().year)

#modify_share
@app.route('/modify/<code>', methods=['POST'])
def modify_share(code):
	if not session.get('logged_in'):
		abort(401)
	if code and request.form['quantity']:
		g.db.execute('UPDATE stock_basics\
					  SET holdingQuantity = ?\
					  WHERE code = ?', [request.form['quantity'], code])
		g.db.commit()
		flash('Share was successfully modified')
	return redirect(url_for('show_shares'))

#del_entry
@app.route('/del', methods=['DELETE'])
def del_share():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('DELETE FROM ENTRIES WHERE ID = ?', [request.form['code']])
	g.db.commit()
	flash('Selected entry was successfully delete')
	return redirect(url_for('show_shares'))           

@app.route('/delete_project', methods=['DELETE'])
def delete_project():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('DELETE FROM projects WHERE title = ?', request.form['title'])
	g.db.commit()
	flash('The project was successfully deleted.')
	return redirect(url_for('Projects'))

@app.route('/add', methods=['POST'])
def add_project():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into projects (title, url, text) values (?, ?, ?)',
				[request.form['title'], request.form['url'], request.form['text']])
	g.db.commit()
	flash('New project was successfully added.')
	return redirect(url_for('Projects'))

