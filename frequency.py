import sys
import json
import ast
import re

def getTweetText(tweet_file):   #returns a list of all tweets
    tweets = []
    for line in tweet_file:
        jsondata = json.loads(line)
        if "text" in jsondata.keys():
            tweets.append(jsondata["text"])
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

def getFrequencies(tweets):
    freq = {}
    occurences = {}

    for tweet in tweets:
        tweet = tweet.encode('utf-8')
        words = filterTweet(tweet) 
        for word in words:
            occurences[word] = 0
            freq[word] = 0.0

    for tweet in tweets:
        tweet = tweet.encode('utf-8')
        wordsInTweet = filterTweet(tweet) #re.split('\W+',tweet)
        for word in wordsInTweet:
            occurences[word] += 1

    totalTerms = len(occurences.keys())

    for term in occurences.keys():
        freq[term] = float(occurences[term])/totalTerms
        print term, freq[term]
    # print occurences
    return freq

def main():
    tweet_file = open(sys.argv[1])
    
    tweets = getTweetText(tweet_file)
    frequencies = getFrequencies(tweets)


if __name__ == "__main__":
    main()