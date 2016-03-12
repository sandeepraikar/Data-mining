# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 19:27:42 2016

@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 1

"""
import os
import math
import operator
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

filtered_dict={}
doc_token_wt={}
wt_tokens={}
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
sw=stopwords.words('english')
file_list=[]
corpus_root = 'D:/MS_UTA/4semester/CSE5334-DataMining/P1/presidential_debates'

#Parse the documents in the corpus and toeknize
for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), "r", encoding='utf-8')     
    tokens = tokenizer.tokenize(file.read().lower())
    filtered_tokens=[stemmer.stem(word) for word in tokens if not word in sw ]   
    filtered_dict[filename]=Counter(filtered_tokens)
    file_list.append(filename)
    file.close() 

#Total number of files in corpus
tot_files = len(file_list)

#This function calculates the idf for a given token
def getidf(token): 
    doc_occ_count=0
    for key,val in filtered_dict.items():
        if(val[token]>0):
            doc_occ_count+=1
    if(doc_occ_count>0):
        return math.log10(tot_files/doc_occ_count)
    else:
        return 0
for filename,tokens_dict in filtered_dict.items():
    for key, value in tokens_dict.items():
        wt_tokens[key]=(1+math.log10(value))*getidf(key)
    doc_token_wt[filename]=wt_tokens
    wt_tokens={}

#This function calculates the cosine normalized wight for a given document
def getcosnormwtdoc(filename):    
    doc_vector=0
    normalized_wt_doc={}
    for key,val in doc_token_wt[filename].items():
        doc_vector+=val*val
    doc_vector=math.sqrt(doc_vector)
            
    for key,val in doc_token_wt[filename].items():
        normalized_wt_doc[key]=val/doc_vector    
    return normalized_wt_doc
    
#This function computes the count of a token in the corpus
def getcount(token):	
    token_count=0
    for key,val in filtered_dict.items():
        token_count+=val[token]
    return token_count

#This function returns the document with the highest similariry with the given query string
def query(qstring):
    result={}
    for filename in file_list:
        result[filename]=querydocsim(qstring,filename)
    return max(result.items(), key=operator.itemgetter(1))[0]   
    
#This function returns the cosine similarity between a query string and a document
def querydocsim(qstring,filename):
    q_tokens=tokenizer.tokenize(qstring)
    clean_tokens=[stemmer.stem(word) for word in q_tokens if word not in stopwords.words('english')]
    query_tcount_dict={}    
    query_dict={}    
    query_tcount_dict=Counter(clean_tokens)
    
    for key, val in query_tcount_dict.items():
        query_dict[key]=1+math.log10(val)
    query_vector=0
    
    for key,val in query_dict.items():
        query_vector+=val*val
    query_vector=math.sqrt(query_vector)
    
    normalized_wt_query={}    
    
    for key,val in query_dict.items():
        normalized_wt_query[key]=val/query_vector
        
    result=0    
    normalized_wt_doc=getcosnormwtdoc(filename)
    for key1,val1 in normalized_wt_doc.items():
        for key,val in normalized_wt_query.items():
            if(key1==key):
                result+=val*val1
    
    return result

#This function returns the cosine similarity between two documents.
def docdocsim(filename1,filename2):
    cosine_weight_doc1=getcosnormwtdoc(filename1)    
    cosine_weight_doc2=getcosnormwtdoc(filename2)    
    result=0
    
    for key1,val1 in cosine_weight_doc1.items():
        for key,val in cosine_weight_doc2.items():
            if(key1==key):
                result+=val*val1
    
    return result
                
# output Set 1
print(query("health insurance wall street"))
print(getcount('health'))
print("%.12f" % getidf("health"))
print("%.12f" % docdocsim("1960-09-26.txt", "1980-09-21.txt"))
print("%.12f" % querydocsim("health insurance wall street", "1996-10-06.txt"))

# output Set 2
'''
print(query("security conference ambassador"))
print(getcount('attack'))
print("%.12f" % getidf("agenda"))
print("%.12f" % docdocsim("1960-10-21.txt", "1980-09-21.txt"))
print("%.12f" % querydocsim("particular constitutional amendment", "2000-10-03.txt"))
'''
# output Set 3
'''
print(query("particular constitutional amendment"))
print(getcount('amend'))
print("%.12f" % getidf("particular"))
print("%.12f" % docdocsim("1960-09-26.txt", "1960-10-21.txt"))
print("%.12f" % querydocsim("health insurance wall street", "2000-10-03.txt"))
'''