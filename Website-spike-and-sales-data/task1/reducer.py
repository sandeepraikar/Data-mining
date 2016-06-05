#!/usr/bin/env python

"""
Created on Sat Apr 23 19:13:13 2016


@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 3
Task1 - reducer
"""

import sys

current_combo = None
combo = None
total_sales =0
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    #dept, year, sales = line.split('\t',2)
    data_mapped = line.strip().split('\t')
    if len(data_mapped) != 3:
        continue
 
    dept,year,sales = data_mapped 
    # convert count (currently a string) to float
    try:
        sales = float(sales)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    combo = str(dept)+"_"+str(year)
    if(current_combo==combo):
        total_sales+=sales
    else:
        if(current_combo):
            if(total_sales>25000000):
                print('%s\t%s\t%s' % (current_combo.split("_")[0],current_combo.split("_")[1],total_sales))
        total_sales=sales
        current_combo=combo

# do not forget to output the last word if needed!
if current_combo == combo:
	print('%s\t%s\t%s' % (current_combo.split("_")[0],current_combo.split("_")[1],total_sales))
     
	
