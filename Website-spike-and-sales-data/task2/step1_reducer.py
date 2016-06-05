#!/usr/bin/env python

"""
Created on Sat Apr 23 19:13:13 2016


@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 3
Task2 - step1_reducer
"""

import sys

current_website = None
website = None
counter = 1.0
avg_time_spent = 0.0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    data_mapped = line.strip().split('\t')
    if len(data_mapped) != 3:
        continue
 
    website,date,time_spent = data_mapped
    # convert count (currently a string) to float
    try:
        time_spent = float(time_spent)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    website=str(website)+"|"+str(date)
    if(current_website==website):
        avg_time_spent+=time_spent
        counter = counter + 1
    else:
        avg_time_spent = avg_time_spent/counter
        if(current_website):
            print('%s\t%s\t%s' % (current_website.split("|")[0],current_website.split("|")[1],avg_time_spent))
        avg_time_spent=time_spent
        current_website=website
        counter=1.0
     
     
	
