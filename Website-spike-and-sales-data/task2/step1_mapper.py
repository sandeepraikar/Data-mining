#!/usr/bin/env python
"""
Created on Sun Apr 24 12:44:46 2016


@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 3
Task2 - step1_mapper
"""

import sys
from datetime import datetime

# input comes from STDIN (standard input)
for line in sys.stdin:
    website,start,end = line.split('\t')
    start_time = start.split(" ")
    end_time = end.split(" ")
    dt1 =datetime.strptime((start_time[1]).strip() , '%H:%M:%S')
    dt2 =datetime.strptime((end_time[1]).strip() , '%H:%M:%S')
    time_spent =dt2-dt1
    print('%s\t%s\t%s' % (website,start_time[0],time_spent.seconds))


