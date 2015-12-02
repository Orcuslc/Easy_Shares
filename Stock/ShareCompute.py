#!/usr/bin/env python
#ShareCompute.py

def Profit(shares):
	count = 0
	profit = 0
	if shares == None:
		return "Please choose shares ASAP."
	for share in shares:
		profit += share['holdingQuantity'] * share['price_change']
		count += 1
	return "Profit rate yesterday is :{0}".format(profit / count)