import sys
import json
import ast
import re
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

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
                scores[word] = float(sentiments[currentIdx])
            else:
                scores[word] = (sentiments[currentIdx] + scores[word])/float(occurences[word])

        currentIdx += 1
    return scores
def initialiseScores():
    statewiseScores = {}
    for state in states.keys():
        statewiseScores[state] = 0
    return statewiseScores

def getHashtags(tweet_file):
    hashtags = {}
    for line in tweet_file:
        jsondata = json.loads(line)
        if "entities" in jsondata.keys():
            if "hashtags" in jsondata["entities"] and len(jsondata["entities"]["hashtags"])>0:
                # print jsondata["entities"]["hashtags"][0]["text"]
                
                hasht = jsondata["entities"]["hashtags"][0]["text"].encode('utf-8')
                
                if hasht in hashtags.keys():
                    hashtags[hasht] += 1
                else:
                    hashtags[hasht] = 1     
    # print hashtags
    count = 0
    for word in sorted(hashtags, key=hashtags.get, reverse=True):   
        print word, hashtags[word]
        count += 1
        if count == 10:
            break
   
def calcStateWiseScores(statewiseScores, tweet_file, sentiments):
    idx = 0
    for line in tweet_file:
        jsondata = json.loads(line)

        if "user" in jsondata.keys():
            loc =  jsondata["user"]["location"].encode('utf-8')
            # print loc
            loc = re.split('\W+',loc)  #re.split('\W+',tweet)
            for place in loc:
                try:
                    if place in states.keys() or place in states.values():
                        statewiseScores[states.get(place)] += sentiments[idx]
                except:
                    pass

        idx += 1
    return statewiseScores

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = calcScoreFromTerm(sent_file)
    statewiseScores = initialiseScores()
    tweets = getTweetText(tweet_file)
    sentiments = getTweetSentiments(tweets, scores)
    tweet_file = open(sys.argv[2])
    statewiseScores = calcStateWiseScores(statewiseScores, tweet_file, sentiments)

    happiestStates = sorted(statewiseScores, key=statewiseScores.get, reverse=True)   
    print happiestStates[0]       

if __name__ == '__main__':
    main()
