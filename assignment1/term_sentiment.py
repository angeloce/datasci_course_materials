#coding:utf-8

import sys
import codecs
import json


phrase_sentiment_sheet = {}
word_sentiment_sheet = {}

unset_term_scores = {}

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


def _is_term(term):
    if term.startswith('#') or term.startswith('@'):
        return False
    if term.startswith('http://t.co'):
        return False
    return True


def find_unset_term_score(tweet):
    sentiment = 0
    unset_terms = set()
    if tweet:
        words = tweet.strip().split()
        for word in words:
            if word in word_sentiment_sheet:
                sentiment += word_sentiment_sheet[word]
            elif _is_term(word):
                unset_terms.add(word)

    for term in unset_terms:
        if term not in unset_term_scores:
            unset_term_scores[term] = [sentiment, 1]
        else:
            unset_term_scores[term][0] += sentiment
            unset_term_scores[term][1] += 1


def print_unset_term_score(filename):
    tweet_file = codecs.open(filename, encoding="utf-8")
    for line in tweet_file:
        tweet = json.loads(line).get('text')
        find_unset_term_score(tweet)

    for term, values in unset_term_scores.items():
        score = float(values[0]) / values[1]
        print "%s %.3f" % (term.encode("utf-8"), score)

    tweet_file.close()


def main():
    set_sentiment_sheet(sys.argv[1])
    print_unset_term_score(sys.argv[2])


if __name__ == '__main__':
    main()
