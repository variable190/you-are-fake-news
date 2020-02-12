import json
from twython import Twython, TwythonError
import requests
import csv
import re
import time

# collect twitter api credentials
with open('twitter_credentials.json') as f:
    creds = json.load(f)
    f.close()

# create twitter api client
client = Twython(creds['consumer_key'], creds['consumer_secret'], \
    creds['access_token'], creds['access_token_secret'])

# define function which adds data to txt file
def save_to_txt(data, label):
    with open('tweets_and_labels.txt', 'a') as file:
        file.write(data + "," + label + "\n")

'''
url = 'theguardian.com'
label = '1'
outlets = {'the guardian', 'guardian'}
'''
url = 'dailymail.co.uk'
label = '0'
outlets = {'mailonline','via'}

# define function to preprocess query results
def process_results(results):
    try:
        for result in results:
            tweet = result['full_text'].encode('utf-8')
            urlsRemoved = re.sub(r'http\S+', '', tweet)
            newlinesRemoved = urlsRemoved.replace('\n', ' ')
            lowered = newlinesRemoved.lower()
            for outlet in outlets:
                outletsRemoved = lowered.replace(outlet, '')
            filtered = re.sub('[^a-z]', ' ', outletsRemoved)
            excessSpacesRemoved = " ".join(filtered.split())
            if not excessSpacesRemoved.isspace():
                save_to_txt(excessSpacesRemoved, label)
            lastId = result['id']-1
    except:
        print(lastId)

# variable to track id of the current tweet being handled
lastId = 0

# conduct initial query and process results
try:
    results = client.cursor(client.search, q=url + ' AND -filter:retweets',\
        tweet_mode='extended',lang='en',count=100)
except TwythonError as e:
    print(e)

process_results(results)

# pause process to prevent reaching maximum queries allowed
time.sleep(30)

# iterate query starting from last tweet handled
while next(results) is not None:
    try:
        results = client.cursor(client.search,q=url+' AND -filter:retweets',\
            tweet_mode='extended',lang='en',count=100,max_id=lastId)
    except TwythonError as e:
        print(e)

    process_results(results)

    time.sleep(10)
