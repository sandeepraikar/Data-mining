#!/usr/bin/env python
"""
Created on Sat Apr 23 18:53:44 2016

@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 3
Task1 - mapper
"""
import sys
import re

# input comes from STDIN (standard input)
for line in sys.stdin:
    store,dept,year,sales = line.split('\t')
    print('%s\t%s\t%s' % (dept, year[0:4], sales))
