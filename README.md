# YouAreFakeNews #

This is a complete basic package for creating datasets of tweets, analysing 
them with deep learning and deploying the trained networks as a REST API.

## Product Prototype ##

This is a self contained proof of concept. There is a script for collecting 
tweets and preprocessing them ready to be fed into a neural network.  An a
basic convoluted neural network built using NumPy.

## Dataset Creation ##

Here are scripts for collecting sets of tweets, manipulating them
collections into datasets and randomising them with a file of corresponding
labels.  There is also a script for flipping labels if so required.

## Neural Network ##

Many models were tested on the satire_vs_serious dataset to find one that fits 
best.  The chosen model was then used on the other datasets.  A selection of 
the models have been uploaded to the Google cloud platform where they can be 
accessed through REST APIs to make predictions.

## Web App ##

The web app is very basic and is purely just to demostrate an interface that
can accept a tweet, process it and semd it to the models through their 
respictive APIs.  The app then presents the returned predictions.


*All scripts that have filepaths are relative as if the script is being run 
from its actual location.

Scripts that connect to the Twitter API require credentials adding to the json
file as instructed.*