'''
Created on March 14, 2017

@author: Ryan Schubert
'''

#!/usr/bin/env python

import sys
import string
import simplejson
from twython import Twython

import datetime
now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)

#OAUTH

t = Twython(app_key='UIdeItVBO6TK1HUDFRwmySCNw', #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret='X1SKdQnIqoMO9ZOD4ib3ZdlC2RFCy8tl5QsPHQrrPpjoqzamOy',
    oauth_token='104657169-euvKE5fpqLr6p3zk72Of5XylMMtw9NvWxtBiCGk4',
    oauth_token_secret='y1pzipRKGtwqoEm3MOugDBukIertbV1myCwx5Fy63hsPJ')

query= 'etown2021'

search = t.search(q=query, count=100)
for tweet in search['statuses']:
    print(tweet['text'])
    #tweets[t] = search[text]
    
print('tweets: \n')

for key in search['statuses'][0].keys():
  print(key)