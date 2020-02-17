import random

# variable to hold name of dataset to be randomised and split
dataset = 'us_left_vs_right'

# Open dataset, enumerate with random number and sort in ascending numerical 
# order
with open('datasets\\' + dataset + '\\tweets_and_labels.txt','r',\
     encoding='utf8') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()

# Write tweets to file and matching label on the respective line in a seperate
# file
for _, line in data:
    tweet_and_label = line.rsplit(',', 1)
    tweet = tweet_and_label[0]
    label = tweet_and_label[1]
    with open('datasets\\' + dataset + '\\tweets.txt','a', encoding='utf8')\
         as tweet_target:
        tweet_target.write(tweet + ' \n')
    with open('datasets\\' + dataset + '\\labels.txt','a') as label_target:
        label_target.write(label)
