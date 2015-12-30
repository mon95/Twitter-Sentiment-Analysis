import sys
import json
import ast
import re

def calcScoreFromTerm(termScoreFile):
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


def getTermByTermSentiments(tweets, scores, sentiments):
    currentIdx = 0      # start with the 1st tweet
    occurences = {}     # to keep track of count of words that we've seen 
    for tweet in tweets:
        tweet = tweet.encode('utf-8')
        words = filterTweet(tweet) #re.split('\W+',tweet)
        
        for word in words:
            occurences[word] = 0

    for tweet in tweets:
        tweet = tweet.encode('utf-8')
        wordsInTweet = filterTweet(tweet) #re.split('\W+',tweet)
        
        for word in wordsInTweet:
            occurences[word] += 1
            if word not in scores:
                scores[word] = float(sentiments[currentIdx])    #Assign the sentiment of the current tweet index
            else:
                scores[word] = (sentiments[currentIdx] + scores[word])/float(occurences[word]) # Assign an averaged value

        currentIdx += 1

    return scores


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = calcScoreFromTerm(sent_file)
    tweets = getTweetText(tweet_file)
    sentiments = getTweetSentiments(tweets, scores)   
    newScores = getTermByTermSentiments(tweets, scores, sentiments)
    
    # print newScores
    for key in newScores.keys():
        if len(key)>=1 and len(key.split(' '))==1:
            print key, newScores[key]
        else:
            nkey = key.split(' ')
            for item in nkey:
                try:
                    print item, newScores[key]
                except:
                    print item, 0.0

if __name__ == '__main__':
    main()
