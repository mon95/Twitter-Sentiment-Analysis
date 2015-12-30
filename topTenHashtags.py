import sys
import json
import ast
import re

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

def main():
    tweet_file = open(sys.argv[1])

    getHashtags(tweet_file)
    

if __name__ == '__main__':
    main()
