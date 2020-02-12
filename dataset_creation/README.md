# Dataset Creation #

This folder holds scripts to collect tweets, assign labels and preprocess the
data.


## Twitter API Credentials ## 

In order to connect to the twitter api the *twitter_credentials.json* file 
needs popoulating with credentials in the following format:
`
{
    "consumer_key": "", 
    "consumer_secret": "", 
    "access_token": "", 
    "access_token_secret": ""
}
`

## Scripts ##

The *twitter_api_iterative_search.py* script collects all tweets for the past
seven days that contain a specified URL.  Any URLs and specified words or 
phrases are removed from the tweets.  If the remaining tweet contains text, a
specified label is added and the tweet is added to a specified filename in the
*collected_tweets* folder.

The *remove_duplicates.py* script creates a new file adding only unique tweets 
as well as a single sample of any duplicates from the a callection of 
raw tweets read from text file.

The *randomise_and_split_from_labels.py* script reads a specified dataset,
randomises the order of the set and outputs two new files one containing the
tweets and another with the labels for each tweet on the corresponding line.