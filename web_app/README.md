# Basic web app example to connect to neural net API

This basic Flask web app provides a form where a tweet can be entered, encoded and passed 
to the neural net REST api.

The Procfile, runtime.txt and requriements.txt file are required to host the web app on heroku.

The GOOGLE_APPLICATION_CREDENTIALS.json file requires credentials to connect to the NN API
which is stored on google cloud platform.

The vocabulary.txt file has the words of the NN embedding layer in the order of their
respective IDs.