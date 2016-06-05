#!/usr/bin/env python
"""
Created on Thu Apr 28 23:42:15 2016


@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 3
Task2 - step2_mapper
"""


import sys
import Queue
from datetime import datetime, timedelta


last_website_enqued=None
last_browse_date=None
count=0
q = Queue.Queue(maxsize=3)

# input comes from STDIN (standard input)
for line in sys.stdin:
    count+=1        
    website,date,seconds = line.split('\t')
    curr_date = datetime.strptime(date.strip(), '%Y-%m-%d').date()
    #populate the queue
    if(not q.full()):
        if(count==1):            
            q.put(website+"|"+date+"|"+seconds)
            last_website_enqued = website
            last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()            
        else:
            computed_date = last_browse_date+timedelta(days=1)        
            #compute the next date from the last record added in the queue
            if(last_website_enqued==website and curr_date==computed_date):
                q.put(website+"|"+date+"|"+seconds)
                last_website_enqued=website
                last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()
            else:
                #clearing the queue
                with q.mutex:
                    q.queue.clear()
                q.put(website+"|"+date+"|"+seconds)
                last_website_enqued=website
                last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()
    else:
        #Now the queue is full and now we can iterate through the queue to find spike
        validation=True
        for i in range(1,q.qsize()):  
            time1 = float(q.queue[i].split('|')[2])
            time2 = float(q.queue[i-1].split('|')[2])
            if(time1>=(time2*2)):
                continue
            else:
                validation=False
                break
            
        if(validation):
            #spike has been observed for 3 consecutive days
            record = q.get()
            q.task_done()
            #dequeue the first record from the queue
            print('%s\t%s' % (record.split('|')[0], 1))
            # adding the current record in the queue!
            computed_date = last_browse_date+timedelta(days=1)                    
            if(last_website_enqued==website and curr_date==computed_date):
                q.put(website+"|"+date+"|"+seconds)
                last_website_enqued=website
                last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()
            else:
                #clearing the queue
                with q.mutex:
                    q.queue.clear()
                q.put(website+"|"+date+"|"+seconds)
                last_website_enqued=website
                last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()
        else:
            #Validation failed, website spike not observed for 3  consecutive days
            q.get()
            q.task_done()
            computed_date = last_browse_date+timedelta(days=1)        
            if(last_website_enqued==website and curr_date==computed_date):
                q.put(website+"|"+date+"|"+seconds)
                last_website_enqued=website
                last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()
            else:
                #clearing the queue
                with q.mutex:
                    q.queue.clear()
                q.put(website+"|"+date+"|"+seconds)
                last_website_enqued=website
                last_browse_date =  datetime.strptime(date, '%Y-%m-%d').date()
            continue
