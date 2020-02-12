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

# Details of what to search for, what to remove from the results, 
# what label to add and the name of the file to write the results to
'''
url = 'theguardian.com'
label = '1'
outlets = {'The Guardian'}
filename = 'guardian.txt'

url = 'dailymail.co.uk'
label = '0'
outlets = {'@MailOnline','Daily Mail Online','@DailyMailCeleb','@Femail','via'}
filename = 'mail.txt'

url = 'wsj.com'
label = '0'
outlets = {'@WSJ','WSJ'}
filename = 'wsj.txt'

url = 'theonion.com OR babylonbee.com'
label = '1'
outlets = {'@TheOnion','@theonion','The Onion','Onion','onion',\
    'The Babylon Bee','@TheBabylonBee','babylon bee','via'}
filename = 'satire.txt'

url = 'newyorker.com'
label = '1'
outlets = {'@NewYorker','@newyorker','via'}
filename = 'newyorker.txt'

url = 'slate.com'
label = '1'
outlets = {'@slate','@Slate','Slate','via'}
filename = 'slate.txt'

url = 'breitbart.com'
label = '0'
outlets = {'@BreitbartNews','via'}
filename = 'breirbart.txt'

url = 'msnbc.com'
label = '1'
outlets = {'@msnbc','@MSNBC','MSNBC','via'}
filename = 'msnbc.txt'
'''
url = 'foxnews.com'
label = '0'
outlets = {'@foxnews','@FoxNews','#FoxNews','Fox News','fox news','via'}
filename = 'foxnews2.txt'

# variable to track id of last tweet collected
lastId = 0

# define function which adds data to txt file
def save_to_txt(data, label):
    with open('collected_tweets\\' + filename, 'a') as file:
        file.write(data + "," + label + "\n")

# function to process result set and write to file
def process_results(results):
    try:
        for result in results:
            tweet = result['full_text'].encode('utf-8')
            urlsRemoved = re.sub(r'http\S+', '', tweet)
            newlinesAndOutletsRemoved = urlsRemoved.replace('\n', ' ')
            for outlet in outlets:
                newlinesAndOutletsRemoved = newlinesAndOutletsRemoved.\
                    replace(outlet, '')
            excessSpacesRemoved = " ".join(newlinesAndOutletsRemoved.split())
            if not excessSpacesRemoved.isspace():
                save_to_txt(excessSpacesRemoved, label)
            global lastId
            lastId = result['id']-1
    except:
        print(lastId)

# conduct intial search and pass results to process_results function
try:
    results = client.cursor(client.search, q=url + ' AND -filter:retweets',\
        tweet_mode='extended',lang='en',count=100)
except TwythonError as e:
    print(e)
process_results(results)

# Pause for 30 seconds before beginning search iteration (pauses stop the query
# limit being reach for the basic twitter API)
time.sleep(30)

# iterate searches, passing the ID of last tweet from previous iteration as 
# max_id parameter
while next(results) is not None:

    try:
        results = client.cursor(client.search,q=url+' AND -filter:retweets',\
            tweet_mode='extended',lang='en',count=100,max_id=lastId)
    except TwythonError as e:
        print(e)
    
    process_results(results)
    
    time.sleep(10)
