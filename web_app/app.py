import tensorflow as tf
from flask import Flask, redirect, url_for, request, render_template
import re
import numpy
import googleapiclient
from oauth2client.client import GoogleCredentials

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('home.html')

@app.route('/results', methods=['POST','GET'])
def analyse_tweet():
    if request.method == 'POST':
        tweet = request.form['tweet']
        tweet = re.sub(r'http\S+', '', tweet)
        tweet = tweet.replace('\n', ' ')
        tweet = tweet + ' \n'
        tweet_list = []
        tweet_list.append(tweet)
        tweet_list.append('<p> '*53 + '\n')
        tweet_list = preprocess(tweet_list)
        tweet_list = encode_words(tweet_list)
        encoded_tweet = tweet_list[0].numpy().tolist()
        project = 'tweet-sentiments-266913'
        model = 'satire_or_real_test'
        prediction = predict_json(project, model, encoded_tweet)
        return render_template('results.html', result=prediction)
    else:
        return redirect(url_for('index'))

def preprocess(tweet):
    tweet = tf.strings.substr(tweet, 0, 240)
    tweet = tf.strings.regex_replace(tweet, b"<br\\s*/?>", b" ")
    tweet = tf.strings.regex_replace(tweet, b"[^a-zA-Z']", b" ")
    tweet = tf.strings.split(tweet)
    return tweet.to_tensor(default_value=b"<p>")

vocabulary = []

with open('vocabulary.txt', 'r') as file:
    for line in file:
        vocabulary.append(line[2:-2])

words = tf.constant(vocabulary)
word_ids = tf.range(len(vocabulary), dtype=tf.int64)
vocab_init = tf.lookup.KeyValueTensorInitializer(words, word_ids)
num_oov_buckets = 1000
table = tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)

def encode_words(dataset_input):
    return table.lookup(dataset_input)

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


if __name__ == '__main__':
    app.run() 