#coding:utf-8

import sys
import codecs
import json




def _is_term(term):
    if term.startswith('#') or term.startswith('@'):
        return False
    if term.startswith('http://t.co'):
        return False
    return True


def print_term_frequency(filename):
    term_occurrences = {}
    total_term_count = 0
    tweet_file = codecs.open(filename, encoding="utf-8")
    for line in tweet_file:
        tweet = json.loads(line).get('text')
        if tweet:
            words = tweet.strip().lower().split()
            for word in words:
                if _is_term(word):
                    if word not in term_occurrences:
                        term_occurrences[word] = 0
                    term_occurrences[word] += 1
                    total_term_count += 1

    for term, occurrences in term_occurrences.items():
        print "%s %.4f" % (term.encode("utf-8"), float(occurrences)/total_term_count)
        

def main():
    print_term_frequency(sys.argv[1])


if __name__ == '__main__':
    main()

