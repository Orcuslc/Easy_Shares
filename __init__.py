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
# DATABASE = '/Users/bohaotang/stock.db'
# DATABASE = '/var/www/Stock/Stock/DataBase/stock.db'
DATABASE = 'E:\\Chuan\\Documents\\GitHub\\Stock\\DataBase\\stock.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DOWNLOAD_FOLDER = 'download'

app.config.from_object(__name__)


from views import *

if __name__ == '__main__':
	app.run(host = '0.0.0.0')
