# Neural Network #

Multiple models are trained on the satire_vs_serious dataset to find one that 
performs the best, this model is used because it is the smallest and smaller 
datasets are more likely to have problems with overfitting. Finding a model
that works well on this dataset suggest it will work better on the others.

The best fitting model was then used for each of the other datasets and the
performance can be seen for each dataset in its respective .ipynb file.  
Each model was then saved as a .h5 file in the saved_models folder.

These models can be trained and tested in Jupyter using Anaconda on Python 3 or 
in a web browser using Googles Colab interface. Tensorflow 2.1 was used, thus, 
if using Colab add `%tensorflow_version 2.x` before the Tensorflow import.
The tweets and labels of the dataset that is to be trained will also need
adding and the filepath amending to locate them correctly. Here is an example of
code that can be added to mount the gdrive and the dataset.

<pre>from google.colab import drive
drive.mount('/content/gdrive')

with open('/content/gdrive/My Drive/Colab Notebooks/tweets.txt', encoding="utf8") as f:
    raw_tweets = f.readlines()
    
with open('/content/gdrive/My Drive/Colab Notebooks/labels.txt') as f:
    raw_labels = f.readlines()</pre>

Once a network has been trained or loaded onto Colab it can be saved to a 
storage bucket on Google Cloud Platform (GCP) using the following code.

<pre>import sys

if 'google.colab' in sys.modules:
  from google.colab import auth as google_auth
  google_auth.authenticate_user()
else:
  %env GOOGLE_APPLICATION_CREDENTIALS ''
  
export_path = tf.saved_model.save(model, 'gs://[bucket]/[model]')</pre>

Once a model has been saved to a storage bucket an API can be created using the
AI platform on GCP.  Three of the models have APIs: moderates_vs_extremes, 
left_vs_right and satire_vs_serious.  The web_app has been built as an example
of processing a tweet to access these models through the APIs.
