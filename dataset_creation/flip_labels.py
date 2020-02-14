import random

# Set source, target, required amount of tweets and required label variables
tweet_set = 'newyorker_dr'
dataset = 'moderate_vs_extremes'
tweets_required = 3706
required_label = "1"

# randomise tweets to prevent using a portion clumped from the same timeframe
with open('collected_tweets\\' + tweet_set + '.txt','r',\
     encoding='utf8') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()

# Remove current label, add new one and write to dateset file
i = 1
for _, line in data:
    if i <= tweets_required:
        tweet_and_label = line.rsplit(',', 1)
        tweet = tweet_and_label[0]
        with open('datasets\\' + dataset + '\\tweets_and_labels.txt','a',\
            encoding='utf8') as tweet_target:
            tweet_target.write(tweet + ','+required_label+'\n')
        i += 1
    else:
        break
