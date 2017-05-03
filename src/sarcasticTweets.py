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
import matplotlib.pyplot as plt
import pandas
import sklearn
import unicodedata
import itertools
from numpy.dual import svd
import time
from posix import fpathconf

reload(sys)
sys.setdefaultencoding('utf8')

def remove_all(element, list):
    return filter(lambda x: x != element, list)

#OAUTH

t = Twython(app_key='UIdeItVBO6TK1HUDFRwmySCNw',
    app_secret='X1SKdQnIqoMO9ZOD4ib3ZdlC2RFCy8tl5QsPHQrrPpjoqzamOy',
    oauth_token='104657169-euvKE5fpqLr6p3zk72Of5XylMMtw9NvWxtBiCGk4',
    oauth_token_secret='y1pzipRKGtwqoEm3MOugDBukIertbV1myCwx5Fy63hsPJ')

#setup query

query = 'sarcasticTweet'
hashtag = '#' + query

#search
search = t.search(q=query, count=100, lang='en', result_type='recent')

#init list that will store tweets
tweets = []

#parse query results for just the tweet body and store in list.
'''for tweet in search['statuses']:
    if tweet['text'].partition(' ')[0] != 'RT' and tweet['text'] != query and tweet['text'] != hashtag and tweet['retweeted'] == False: 
        tweets.append(tweet['text'])

time.sleep(10)mystr[-4:]mystr[-4:]mystr[-4:]mystr[-4:]

search = t.search(q=query, count=100, lang='en', result_type='recent')
for tweet in search['statuses']:
    if tweet['text'].partition(' ')[0] != 'RT' and tweet['text'] != query and tweet['text'] != hashtag and tweet['retweeted'] == False: 
        tweets.append(tweet['text'])
'''

with open('tweetDataSet.txt') as f:
    tweets = f.readlines()

#tweets.append("Nothing better than taking a super difficult exam that you're not prepared for!")
sar_tweets = []

for tweet in tweets:
    if "*y*" in tweet:
        sar_tweets.append(tweet)
        tweets.remove(tweet)
        
#init tokens list  
org_tokens = []

#tokenize tweets
for tweet in tweets:
    org_tokens.append(word_tokenize(tweet))

for t in org_tokens:
    print t

for tweet in org_tokens:
    for i,t in enumerate(tweet):
        if t.isalnum() != True:
            tweet.remove(t)

'''print "\nafter rem---------------\n"
 
for t in org_tokens:
    print t
    
    
print '\n\n-------------------------------------------------------------\n\n'

'''

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
#print sent_dict.items()[0][1]
       
values = []
lengths = []
arousal = []
valence = []
fpv = []
fpvl = []
fpa = []
fpva = []

for i,(k,v) in enumerate(sent_dict.items()):
    sv = v[1][1] - v[0][1]
    val = v[1][1]
    aro = v[0][1]
    sl = len(sent_dict.items()[i][0].split())
    if sv >= 1.6 and sl >= 5.8:
        fpv.append(sv)
        fpvl.append(sl)
        fpa.append(aro)
        fpva.append(val)
    else:
        values.append(sv)
        lengths.append(sl)
        arousal.append(aro)
        valence.append(val)

    if sv < .5:
        print "NOT SARCASTIC" + " (" + str(sl) +"): " + sent_dict.items()[i][0] + "\n"
    if sv > .5 and sv < 1:
        print "PROBABLY NOT SARCASTIC" + " (" + str(sl) +"): " + sent_dict.items()[i][0] + "\n"
    if sv > 1 and sv < 2:
        print "MAYBE SARCASTIC" + " (" + str(sl) +"): " + sent_dict.items()[i][0] + "\n"
    if sv > 2:
        print "PROBABLY SARCASTIC" + " (" + str(sl) +"): " + sent_dict.items()[i][0] + "\n"
        
#init tokens list  
org_tokens = []

#tokenize tweets
for tweet in sar_tweets:
    org_tokens.append(word_tokenize(tweet))

#for t in org_tokens:
    #print t

for tweet in org_tokens:
    for i,t in enumerate(tweet):
        if t.isalnum() != True:
            tweet.remove(t)
            
#init sentiments list
sentiments = []

#get avg sentiments for the tweets
for t in org_tokens:
    sentiments.append(sentiment.sentiment(t).items())

sent_dict = {}
for i in range(len(sar_tweets)):
    sent_dict[sar_tweets[i]] = sentiments[i]
    
for k,v in sent_dict.items():
    if v[0][1] < 1 or v[1][1] < 1:
        del sent_dict[k]
       
#print sent_dict.items()[0][0]
#print sent_dict.items()[0][1]
       
sar_values = []
sar_lengths = []
sar_arousal = []
sar_valence = []

for i,(k,v) in enumerate(sent_dict.items()):
    sv = v[1][1] - v[0][1]
    val = v[1][1]
    aro = v[0][1]
    sl = len(sent_dict.items()[i][0].split())
    sar_values.append(sv)
    sar_lengths.append(sl)
    sar_arousal.append(aro)
    sar_valence.append(val)
    
plt.plot(arousal, valence, 'ro')
#plt.plot(fpa, fpva, 'go')
plt.plot(sar_arousal, sar_valence, 'bo')
plt.axis([2, 8, 2, 8])
plt.xlabel('arousal')
plt.ylabel('valence')
plt.show()

x = 0

for val in sar_values:
    if val >= 1.5:
        x = x + 1
        
y = 0

for val in values:
    if val >= 1.5:
        y = y + 1

print "sarcastic:"       
print x
print len(sar_values)
print"\n"
print y
print len(values)



#for key in search['statuses'][0].keys():
 # print(key)