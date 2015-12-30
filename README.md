# Twitter-Sentiment-Analysis
Use the WordNet generated sentiment scores to perform a sentiment analysis of live twitter data, derive sentiments of new terms based on existing knowledge and predict ‘happiest’ states based on sentiment scores.

Here, we 
  1.  Access the twitter Application Programming Interface(API) using python
  2.  Estimate the public's perception (the sentiment) of a particular term or phrase
  3.  Analyze the relationship between location and mood based on a sample of twitter data

###1. Getting Twitter data

Here, we work with the live Twitter stream using the development API. To access the live stream, you will need to install the oauth2 library so you can properly authenticate.

  Use : `pip install oauth2` on the linux command line to perform the installation.
  
The steps below will help you set up your twitter account to be able to access the live 1% stream.

  1.  Create a twitter account if you do not already have one.
  2.  Go to https://dev.twitter.com/apps and log in with your twitter credentials.
  3.  Click "Create New App"
  4.  Fill out the form and agree to the terms.
  5.  On the next page, click the "Keys and Access Tokens" tab along the top, then scroll all the way down until you see the section "Your Access Token"
  6.  Click the button "Create My Access Token". 
  7.  You will now copy four values into the file twitterstream.py. These values are your "Consumer Key (API Key)", your "Consumer Secret (API Secret)", your "Access token" and your "Access token secret". All four should now be visible on the "Keys and Access Tokens" page.
  8.  Open the file "twitterstream.py" and set the variables corresponding to the api key, api secret, access token, and access secret. 
  ```python
      api_key = "<Enter api key>" 
      api_secret = "<Enter api secret>"
      
      access_token_key = "<Enter your access token key here>" 
      access_token_secret = "<Enter your access token secret here>"
  ```

  9. Now, run the following command to get live twitter data into a text file: (wait for a couple of minutes to get the required data)
      `python twitterstream.py > output.txt`

###2. Deriving tweet sentiments:

  The sentiment of a tweet is computed as the sum of the sentiment scores for each term in the tweet.
  Use *AFFIN-111.txt* for the sentiment scores of each term. Copy the first few lines of *output.txt* for sample data(this is the data in *tweet_file*).
  
  Run: `python tweet_sentiment.py AFINN-111.txt tweet_file` to get the tweet sentiments
  
###3. Deriving sentiments of new terms:

  Run: `python term_sentiment.py AFINN-111.txt tweet_file` to get the sentiments for the new terms (i.e., terms not in AFFIN-111.txt)
  
###4. Computing term frequencies:

  The script frequency.py is used to compute the term frequency histogram of the livestream data harvested in 1.

  The frequency of a term can be calculated as :
  [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]
  
  Run: `python frequency.py tweet_file` to get the frequencies
  
###5. Happiest State:

  The script happiest_state.py that returns the name of the happiest state as a string.
  
  Run: `python happiestStates.py AFFIN-111.txt three_minutes_tweets.json` to get the two letter abbreviation of the happiest state in the US based on the tweet sentiments.
  
###6. Top ten Hashtags:

  Run: `python topTenHashtags.py tweet_file` to retrieve the top ten hashtags found in the tweet file
  
  

This assignment was done as part of the "Data Manipulation at Scale: Systems and Algorithms" course (Part of the data science specialization certificate) offered by the University of Washington on Coursera. 

The links and explanations and some sample code for the assignment is used as is from the course website. 

As a side note, I would recommend this course to anyone interested in working on data science problems and looking for some cool work to enhance their skills. 

Link to the same: https://www.coursera.org/learn/data-manipulation/home/welcome
