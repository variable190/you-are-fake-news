import tensorflow as tf
from flask import Flask, redirect, url_for, request, render_template
import re
import numpy
import googleapiclient
from oauth2client.client import GoogleCredentials

app = Flask(__name__)


# preload vocabulary and create lookup tables
num_oov_buckets = 1000

sor_vocabulary = []
with open('sor_vocabulary.txt', 'r') as file:
    for line in file:
        sor_vocabulary.append(line[2:-2])
sor_words = tf.constant(sor_vocabulary)
sor_word_ids = tf.range(len(sor_vocabulary), dtype=tf.int64)
sor_vocab_init = tf.lookup.KeyValueTensorInitializer(sor_words, sor_word_ids)
sor_table = tf.lookup.StaticVocabularyTable(sor_vocab_init, num_oov_buckets)

mve_vocabulary = []
with open('mve_vocabulary.txt', 'r') as file:
    for line in file:
        mve_vocabulary.append(line[2:-2])
mve_words = tf.constant(mve_vocabulary)
mve_word_ids = tf.range(len(mve_vocabulary), dtype=tf.int64)
mve_vocab_init = tf.lookup.KeyValueTensorInitializer(mve_words, mve_word_ids)
mve_table = tf.lookup.StaticVocabularyTable(mve_vocab_init, num_oov_buckets)


# remove urls and preprocess tweet, add to list with fully padded tweet
# of maximum expected embedding size
def encode_tweet(tweet, embed_size, table):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = tweet.replace('\n', ' ')
    tweet = tweet + ' \n'
    tweet_list = []
    tweet_list.append(tweet)
    tweet_list.append('<p> '*embed_size + '\n')
    tweet_list = preprocess(tweet_list, embed_size)
    tweet_list = encode_words(tweet_list, table)
    return tweet_list[0].numpy().tolist()


# preprocess tweet by removing special characters and padding to match maximum
# embedding size
def preprocess(tweet, embed_size):
    tweet = tf.strings.substr(tweet, 0, 240)
    tweet = tf.strings.regex_replace(tweet, b"<br\\s*/?>", b" ")
    tweet = tf.strings.regex_replace(tweet, b"[^a-zA-Z']", b" ")
    tweet = tf.strings.split(tweet, maxsplit=embed_size)
    return tweet.to_tensor(default_value=b"<p>")


# replace words in tweet with respective IDs based on the prediction model it
# is to be passed to
def encode_words(dataset_input, table):
    if table=='sor':
        return sor_table.lookup(dataset_input)
    else:
        return mve_table.lookup(dataset_input)


# pass encoded tweet as HTTP post request to trained NN model API
def predict_json(project, model, instances, version=None):

    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)
    
    response = service.projects().predict(
        name=name,
        body={"instances":[{"embedding_input": instances}]}
    ).execute()
    

    if 'error' in response:
        raise RuntimeError(response['error'])
    
    prediction = round(response['predictions'][0]['dense'][0]*100, 5)

    return prediction


# render home page
@app.route('/')
def index():
   return render_template('home.html')


# preprocess tweet, send it to NN model API and pass the results to 
# be rendered on the results page
@app.route('/results', methods=['POST','GET'])
def analyse_tweet():
    if request.method == 'POST':
        project = 'tweet-sentiments-266913'
        tweet = request.form['tweet']

        encoded_tweet_sor = encode_tweet(tweet, 53, 'sor')
        sor_model = 'satire_or_real_test'
        sor_prediction = predict_json(project, sor_model, encoded_tweet_sor)

        encoded_tweet_mve = encode_tweet(tweet, 51, 'mve')
        mve_model = 'moderate_or_extreme'
        mve_prediction = predict_json(project, mve_model, encoded_tweet_mve)

        return render_template('results.html', sor_result=sor_prediction,\
             mve_result=mve_prediction)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run() 