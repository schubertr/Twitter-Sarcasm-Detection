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

#OAUTH

t = Twython(app_key='UIdeItVBO6TK1HUDFRwmySCNw',
    app_secret='X1SKdQnIqoMO9ZOD4ib3ZdlC2RFCy8tl5QsPHQrrPpjoqzamOy',
    oauth_token='104657169-euvKE5fpqLr6p3zk72Of5XylMMtw9NvWxtBiCGk4',
    oauth_token_secret='y1pzipRKGtwqoEm3MOugDBukIertbV1myCwx5Fy63hsPJ')

#setup query

query = '#sarcasm'
hashtag = '#' + query

numOfResults = 100

#search
search = t.search(q=query, count=numOfResults)

#init list that will store tweets
tweets = []

#parse query results for just the tweet body and store in list.
for tweet in search['statuses']:
    if tweet['text'].partition(' ')[0] != 'RT' and tweet['text'] != query and tweet['text'] != hashtag: 
        tweets.append(tweet['text'])

#init tokens list  
org_tokens = []

#tokenize tweets
for tweet in tweets:
    org_tokens.append(word_tokenize(tweet))

#print tokens    
for t in org_tokens:
    print t
    
print '\n\n-------------------------------------------------------------\n\n'

#init sentiments list
sentiments = []

#get avg sentiments for the tweets
for t in org_tokens:
    sentiments.append(sentiment.sentiment(t).items())

#combine sentiment and token lists 
stokens = [None]*(len(org_tokens)+len(sentiments))
stokens[::2] = org_tokens
stokens[1::2] = sentiments

#print lists
for t in stokens:
    print t

#for key in search['statuses'][0].keys():
 # print(key)