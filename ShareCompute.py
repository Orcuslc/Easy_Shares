#!/usr/bin/env python
#ShareCompute.py

def Profit(shares):
	if shares:
		profit = 0
		asset = 0
		for share in shares:
			asset += ( share['close'] - share['price_change'] ) * share['holdingQuantity'] 
			profit += share['holdingQuantity'] * share['price_change']
		return "Profit rate yesterday is :{0}".format(profit / asset * 100)
	else: return "Please choose shares ASAP."
