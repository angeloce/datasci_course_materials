#coding:utf-8

import sys
import codecs
import json


phrase_sentiment_sheet = {}
word_sentiment_sheet = {}


def set_sentiment_sheet(filename):
    sent_file = codecs.open(sys.argv[1], encoding="utf-8")

    for line in sent_file:
        word, score = line.split('\t', 1)
        try:
            word = word.strip()
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


def print_sentiment(filename):
    tweet_file = codecs.open(filename, encoding="utf-8")
    for line in tweet_file:
        sentiment = 0
        tweet = json.loads(line).get('text')
        if tweet:
            index = 0
            while index < len(tweet):
                word_end_index = tweet.find(' ', index)
                if word_end_index < 0:
                    break
                word = tweet[index:word_end_index]

                if word in word_sentiment_sheet:
                    sentiment += word_sentiment_sheet[word]
                elif word in phrase_sentiment_sheet:
                    for phrase in phrase_sentiment_sheet[word]:
                        if tweet[index:].startswith(phrase):
                            word_end_index = tweet.find(' ', index + len(phrase))
                            sentiment += phrase_sentiment_sheet[word][phrase]
                            break
                index = word_end_index + 1
        print sentiment

    tweet_file.close()


def main():
    set_sentiment_sheet(sys.argv[1])
    print_sentiment(sys.argv[2])


if __name__ == '__main__':
    main()
