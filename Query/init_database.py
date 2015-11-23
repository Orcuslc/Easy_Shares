#get_data

import tushare as ts
import sqlite3 as sql3
import sqlalchemy as sqlalc
import pandas as pd 

engine = sqlalc.create_engine('sqlite:///F:\\Documents\\GitHub\\StockQuerySystem\\Query\\DataBase\\stock.db')

stock_basics = ts.get_stock_basics()
stock_concept = ts.get_concept_classified()

# stock_info_industry_class.to_sql('stock_info_industry_class', engine, if_exists = 'replace', index = "False", index_label = ['code', 'name', 'industry'])
# stock_info = 
# stock_info_concept_class.to_sql('stock_info_concept_class', engine, if_exists = 'replace', index = "False", index_label = ['code', 'name', 'concept'])
# stock_info = pd.merge(stock_info_concept_class, stock_info_industry_class, how = 'outer', on = 'code')
# stock_info = stock_info.drop('name_x',axis = 1)
# stock_info = stock_info.rename(columns={'c_name_x':"概念",'name_y':"名称",'c_name_y':"行业"})
# stock_info.to_sql('stock_info', engine, if_exists = 'replace')

stock_basics.to_sql('stock_basics', engine, if_exists = 'replace')
stock_concept.to_sql('stock_concept', engine, if_exists = 'replace')

for