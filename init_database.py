#! /usr/bin/python3
#coding = 'UTF-8'
#get_data

import tushare as ts
import sqlite3 as sql3
import sqlalchemy as sqlalc
import pandas as pd 

route = 'sqlite:///F:\\Documents\\GitHub\\StockQuerySystem\\Stock\\DataBase\\stock.db'
engine = sqlalc.create_engine(route)


stock_basics = pd.read_sql('SELECT * from stock_basics', engine)
if stock_basics.empty == True:
	stock_basics = ts.get_stock_basics()
	stock_concept = ts.get_concept_classified()
	stock_basics.to_sql('stock_basics', engine, if_exists = 'replace')
	stock_concept.to_sql('stock_concept', engine, if_exists = 'replace')

for stock in stock_basics['code']:
	try:
		stock_price = ts.get_hist_data(stock)
		stock_price.loc[:, 'code'] = stock
		index = stock_price.index
		stock_price = stock_price.set_index(['code', index])
		print(stock_price.index)
		stock_price.to_sql('stock_price', engine, if_exists = 'append')
	except AttributeError:
		print("AttributeError", stock)
		continue
