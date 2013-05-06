#coding:utf-8

import sys
import codecs
import json


phrase_sentiment_sheet = {}
word_sentiment_sheet = {}


def is_wanted_tweet(data):
    if data:
        try:
            if data.get('text') and data.get('place') and data.get('lang') == 'en':
                if data['place']['country_code'] == 'US' and data['place']['full_name']:
                    return True
        except:
            return False
    return False


def set_sentiment_sheet(filename):
    sent_file = codecs.open(sys.argv[1], encoding="utf-8")

    for line in sent_file:
        word, score = line.split('\t', 1)
        try:
            word = word.lower().strip()
            score = float(score.strip())
        except:
            continue
        if ' ' in word:
            first_word = word.split(' ', 1)[0]
            if first_word not in phrase_sentiment_sheet:
                phrase_sentiment_sheet[first_word] = {}
            phrase_sentiment_sheet[first_word][word] = score
        else:
            word_sentiment_sheet[word] = score

    sent_file.close()


def get_sentiment(tweet):
    sentiment = 0
    index = 0
    if tweet:
        tweet = tweet.lower()
        while index < len(tweet):
            word_end_index = tweet.find(' ', index)
            if word_end_index < 0:
                word_end_index = len(tweet)
            word = tweet[index:word_end_index]

            if word in word_sentiment_sheet:
                sentiment += word_sentiment_sheet[word]
            # phrase match
            elif word in phrase_sentiment_sheet:
                for phrase in phrase_sentiment_sheet[word]:
                    if tweet[index:].startswith(phrase):
                        word_end_index = tweet.find(' ', index + len(phrase))
                        sentiment += phrase_sentiment_sheet[word][phrase]
                        break
            index = word_end_index + 1
    return sentiment


def print_happiest_state(filename):
    tweet_file = codecs.open(filename, encoding="utf-8")

    state_sentiment = {}
    for line in tweet_file:
        tweet_data = json.loads(line)
        if is_wanted_tweet(tweet_data):
            state = tweet_data['place']['full_name'][-2:]
            sentiment = get_sentiment(tweet_data.get('text'))
            if state not in state_sentiment:
                state_sentiment[state] = 0
            state_sentiment[state] += sentiment

    tweet_file.close()

    # happiest_state
    if state_sentiment:
        print max(state_sentiment.items(), key=lambda x: x[1])[0]
    else:
        print "US"


def main():
    set_sentiment_sheet(sys.argv[1])
    print_happiest_state(sys.argv[2])


if __name__ == '__main__':
    main()

