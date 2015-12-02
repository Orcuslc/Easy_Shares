#!/usr/bin/env python
#ShareCompute.py

def Profit(shares):
	count = 0
	profit = 0
	for share in shares:
		profit += share['holdingQuantity'] * share['price_change']
		count += 1
	return profit / count