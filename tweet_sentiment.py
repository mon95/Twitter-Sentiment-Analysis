import sys
import json
import ast
import re

def calcScoreFromTerm(termScoreFile):   # returns a dictionary with term-score values
    scores ={}
    for line in termScoreFile:
        term, score = line.split("\t")
        scores[term] = float(score)
    return scores

def getTweetText(tweet_file):   #returns a list of all tweets
    tweets = []
    for line in tweet_file:
        # print line
        jsondata = json.loads(line)
        if "text" in jsondata.keys():
            tweets.append(jsondata["text"])
    tweet_file.close()
    return tweets

def filterTweet(et):
    # Remove punctuations and non-alphanumeric chars from each tweet string
    pattern = re.compile('[^A-Za-z0-9]+')
    et = pattern.sub(' ', et)
    #print encoded_tweet

    words = et.split()

    # Filter unnecessary words
    for w in words:
        if w.startswith("RT") or w.startswith("www") or w.startswith("http"):
            words.remove(w)

    return words

def getTweetSentiments(tweets, scores):     #returns a list of sentiments
    sentiments = []

    for tweet in tweets:
        sentiment = 0.0
        tweet = tweet.encode('utf-8')
        wordsInTweet = filterTweet(tweet) # re.split('\W+',tweet)
        for eachWord in wordsInTweet:
            if eachWord in scores:
                sentiment += scores[eachWord]
        sentiments.append(sentiment)

    return sentiments

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = calcScoreFromTerm(sent_file)
    tweets = getTweetText(tweet_file)
    sentiments = getTweetSentiments(tweets, scores)
    
    for sentiment in sentiments:
        print sentiment

if __name__ == '__main__':
    main()
