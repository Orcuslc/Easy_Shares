"""
The flask application package.
"""

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sqlite3
from contextlib import closing
# from FlaskWebProject1.ShareCompute import *


app = Flask(__name__)

# configuration
DATABASE = '/Users/bohaotang/stock.db'
# DATABASE = '/var/www/Stock/Stock/DataBase/stock.db'
#DATABASE = 'F:\\Documents\\GitHub\\Stock\\DataBase\\stock.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)


from views import *

if __name__ == '__main__':
	app.run(host = '0.0.0.0')
