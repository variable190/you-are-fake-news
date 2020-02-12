# choose dataset to remove duplicates from
tweet_set = 'wsj'

# create set variable to lines two
duplicates_removed = set()

# read in each line and add to the set which will remove duplicates 
with open('collected_tweets\\' + tweet_set + '.txt','r',\
    encoding="utf8") as source:
    for line in source:
        # for this dataset each line was also made lowercase
        duplicates_removed.add(line)

# write each unique line to a new file
for tweet in duplicates_removed:
    with open('collected_tweets\\' + tweet_set + '_dr.txt', 'a', \
        encoding="utf8") as file:
        file.write(tweet)
