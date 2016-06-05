#!/usr/bin/env python
"""
Created on Thu Apr 28 23:42:57 2016


@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 3
Task2 - step2_mapper
"""

import sys

current_website = None
website = None
total_spike_count = 0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    data_mapped = line.strip().split('\t')
    if len(data_mapped) != 2:
        continue
 
    website,spike_count = data_mapped
    # convert count (currently a string) to float
    try:
        spike_count = int(spike_count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    if current_website == website:
        total_spike_count += spike_count
    else:
        if current_website:
            # write result to STDOUT
            print('%s\t%s' % (current_website, total_spike_count))
        total_spike_count = spike_count
        current_website = website
# do not forget to output the last word if needed!
if current_website == website:
    print('%s\t%s' % (current_website, total_spike_count))
