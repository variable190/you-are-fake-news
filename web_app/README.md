# Basic web app example to connect to neural net API #

This basic Flask web app provides a form where a tweet can be entered, encoded 
and passed to the neural net REST api.  The results are then presented to the 
user in a basic format but shows an example of how front end web app 
designers could represent the information.

The Procfile, runtime.txt and requriements.txt file are required to host the 
web app on heroku.

The GOOGLE_APPLICATION_CREDENTIALS.json file requires credentials to connect 
to the NN API which is stored on google cloud platform.

The sor_vocabulary.txt, lvr_vocabulary.txt and mve_vocabulary.txt files have 
the words of the NN embedding layer in the order of their respective IDs.

This app can be tested at https://salty-shelf-21511.herokuapp.com/ it may 
take a little time to load up and make the first request but will run 
smoothly once it has woken up.
