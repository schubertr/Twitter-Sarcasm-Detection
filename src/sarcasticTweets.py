'''
Twitter sentiment analysis/sarcasm trend detection

@author: Ryan Schubert
'''

#!/usr/bin/env python

import sys
import string
import simplejson
from twython import Twython
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from sentiment_module import sentiment
import scipy
import numpy
import matplotlib
import pandas
import sklearn
import unicodedata
import itertools

def remove_all(element, list):
    return filter(lambda x: x != element, list)

#OAUTH

t = Twython(app_key='UIdeItVBO6TK1HUDFRwmySCNw',
    app_secret='X1SKdQnIqoMO9ZOD4ib3ZdlC2RFCy8tl5QsPHQrrPpjoqzamOy',
    oauth_token='104657169-euvKE5fpqLr6p3zk72Of5XylMMtw9NvWxtBiCGk4',
    oauth_token_secret='y1pzipRKGtwqoEm3MOugDBukIertbV1myCwx5Fy63hsPJ')

#setup query

query = 'trump'
hashtag = '#' + query

numOfResults = 100

#search
search = t.search(q=query, count=numOfResults)

#init list that will store tweets
tweets = []

stop_words = open('minimal-stop.txt').read().splitlines()

#parse query results for just the tweet body and store in list.
for tweet in search['statuses']:
    if tweet['text'].partition(' ')[0] != 'RT' and tweet['text'] != query and tweet['text'] != hashtag: 
        tweets.append(tweet['text'])
        
#for tweet in tweets:
#    print tweet

#init tokens list  
org_tokens = []

#tokenize tweets
for tweet in tweets:
    org_tokens.append(word_tokenize(tweet))
print "\nbefore rem---------------\n"

for t in org_tokens:
    print t

for tweet in org_tokens:
    for i,t in enumerate(tweet):
        if t.isalnum() != True:
            tweet.remove(t)

for t in org_tokens:
    for sw in stop_words:
        remove_all(sw, t)

print "\nafter rem---------------\n"
 
for t in org_tokens:
    print t
    
    
print '\n\n-------------------------------------------------------------\n\n'

#init sentiments list
sentiments = []

#get avg sentiments for the tweets
for t in org_tokens:
    sentiments.append(sentiment.sentiment(t).items())

sent_dict = {}
for i in range(len(tweets)):
    sent_dict[tweets[i]] = sentiments[i]
    
for k,v in sent_dict.items():
    if v[0][1] < 1 or v[1][1] < 1:
        del sent_dict[k]
       
#print sent_dict.items()[0][0]
       
for i,(k,v) in enumerate(sent_dict.items()):
    sv = v[1][1] - v[0][1]
    if sv < .5:
        print "NOT SARCASTIC: " + sent_dict.items()[i][0] + "\n"
    if sv > .5 and sv < 1:
        print "PROBABLY NOT SARCASTIC: " + sent_dict.items()[i][0] + "\n"
    if sv > 1 and sv < 2:
        print "MAYBE SARCASTIC: " + sent_dict.items()[i][0] + "\n"
    if sv > 2:
        print "PROBABLY SARCASTIC: " + sent_dict.items()[i][0] + "\n"

#for key in search['statuses'][0].keys():
 # print(key)