#!/usr/bin/env python
#ShareCompute.py

def Profit(shares):
	if shares:
		count = 0
		profit = 0
		for share in shares:
			profit += share['holdingQuantity'] * share['price_change']
			count += 1
		return "Profit rate yesterday is :{0}".format(profit / count)
	else: return "Please choose shares ASAP."