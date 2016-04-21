# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 18:21:25 2016

@author: Sandeep Raikar
UTA ID: 1001103332

CSE5334 - DataMining | Programming assignment - 2

"""

__author__ = 'sandeepraikar'

import datetime
import math
import csv
import pandas as pd
import operator
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
sw=stopwords.words('english')
stemmer = PorterStemmer()

start = datetime.datetime.now().replace(microsecond=0)
print("Start time :", start)

# Pre processing data 
df_train = pd.read_csv('train.csv', encoding="ISO-8859-1")
df_test = pd.read_csv('test.csv', encoding="ISO-8859-1")
df_prod_desc = pd.read_csv('product_descriptions.csv')
df_attr = pd.read_csv('attributes.csv',encoding="ISO-8859-1")

print('Training data lenght :',len(df_train.index))

df_brand = df_attr[df_attr.name == "MFG Brand Name"][["product_uid", "value"]].rename(columns={"value": "brand"})
df_material = df_attr[df_attr.name == "Material"][["product_uid", "value"]].rename(columns={"value": "material"}) 


prior_prob_relevance={}
def calculate_prior_prob():
    relevance_dict = Counter(df_train.relevance)
    class_count = len(relevance_dict)
    total_records = len(df_train.index)    
    #Laplace smoothing applied for Prior probabilities
    for key, val in relevance_dict.items():
        prior_prob_relevance[key] = (val +1) / (total_records +class_count)

def filter(description):   
    tokens = tokenizer.tokenize(description.lower())
    filtered_tokens=[stemmer.stem(word) for word in tokens if not word in sw ]   
    #filtered_dict[filename]=Counter(filtered_tokens)
    return filtered_tokens

    
train_rel_count={}
relevance_df_dict={}
train_data_extract={}
formatted_relevance_dict={}
train_clean_data={}
token_class_count_dict={}
token_dict={}   
vocab_dict={}     
cond_prob_class={}
cond_prob_text={}   
vocab_list=[] 
def train_multinomial_nb(df_target_train):
    df_target_train = df_target_train[['merged','relevance']].groupby('relevance',as_index=False)

    for key,group in df_target_train: 
        #print(key,' --  ',len(group))
        train_rel_count[key]=len(group)
        relevance_df_dict[key]=group        
    
    #Concatenate grouped relevance
    for key, df_temp in relevance_df_dict.items():
        #print(key, '-|-',len(df_temp))   
        formatted_relevance_dict[key]=df_temp.groupby('relevance')['merged'].apply(' '.join).reset_index()
        
    for key, val in formatted_relevance_dict.items():
        del val['relevance']    
        train_data_extract[key]=val.iat[0,0]    

    #Perform stemming and stop words removal
    print("Performing stemming and stop words removal")      
    for key,val in train_data_extract.items():
        print("Performing filter for key: ",key)
        train_clean_data[key]=filter(val)        
        
    #compute length
    for key,val in train_clean_data.items():
        token_class_count_dict[key]=len(val)
        
    for key,val in train_clean_data.items():
        token_dict[key]=Counter(val)

    
    print("Train_multinomial_nb")
    #extracting  vocab
    for key,val in token_dict.items():
        vocab_dict.update(val)
    vocab_len = len(vocab_dict)
    print("Vocab length: ",vocab_len)
    

    count=0
    for word in vocab_dict.values():
        count+=1
    print("Total words in vocab_dict",count)
    
    for word in vocab_dict.keys():
        vocab_list.append(word)
        for key,value in prior_prob_relevance.items():    
            class_dict=token_dict[key]
            len_class_dict=token_class_count_dict[key]
            cond_prob_class[key]=(class_dict.get(word,0)+1)/(len_class_dict+vocab_len)
        cond_prob_text[word]=cond_prob_class
        
    print("Length of cond_prob_text:",len(cond_prob_text))
    print("Vocab_list count",len(vocab_list))


def data_preprocessing(df):    
    df = pd.merge(df, df_prod_desc, how='left', on='product_uid')
    print('after prod desc  length :',len(df.index))
    df = pd.merge(df, df_brand, how='left', on='product_uid')
    print('after brand  length :',len(df.index))
    #Merge all the candidate columns into a single column
    df['merged'] = df['product_title'].map(str)+" "+df['search_term'].map(str)+" "+ df['product_description'].map(str)+" "+df['brand'].map(str)
    print('post merge length :',len(df.index))
    del df['product_title']
    del df['search_term']
    del df['brand']
    del df['product_description']
    del df['product_uid']
    return df

def prior_prob_log():
    log_prob={}    
    for key, val in prior_prob_relevance.items():
        log_prob[key]=math.log10(val)
    return log_prob
    
def extract_common_tokens_vocab(search_tokens):
    return set(search_tokens).intersection(vocab_list)

def filter_processed_test_data(df):
    lambda x: filter(x)
    df['merged'] = df['merged'].apply(filter)
    return df

#Data Preprocessing!
processed_train_df = data_preprocessing(df_train)
processed_test_df = data_preprocessing(df_test)

def multinomial_nb():
    print('preparing model....')
    calculate_prior_prob()          
    train_multinomial_nb(processed_train_df)

def apply_multinomial_nb():
    print('Start classifying test data...')
    df_test_processed = filter_processed_test_data(processed_test_df)
    print("Length after data processing:",len(df_test_processed))    
    print("Completed pre-processing on test data...")
    prior_prob = prior_prob_log()    
    result={}
    for index,row in df_test_processed.iterrows():
        search_tokens= row['merged']
        id=row['id']
        list = extract_common_tokens_vocab(search_tokens)
        score={}
        for key,value in prior_prob.items():
            score[key]=prior_prob[key]
            for word in list:            
                score[key]+=math.log10(cond_prob_text.get(word).get(key))
        result[id]=max(score.items(), key=operator.itemgetter(1))[0] 
    print("Lenght of result :",len(result))       
    
    f = open("submission.csv", "w",newline='')
    writer = csv.writer(f)
    writer.writerow(['id', 'relevance'])
    for key, value in result.items():
        writer.writerow([key, value])
    f.close()

# Multinomial Naive Bayes ###

multinomial_nb()
apply_multinomial_nb()

end = datetime.datetime.now().replace(microsecond=0)


print("End time :", start)
print("Total duration :", (end - start))