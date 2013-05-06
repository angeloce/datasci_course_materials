#coding:utf-8

import sys
import codecs
import json


def print_top_ten_hashtag(filename):
    hashtag_occurrences = {}
    tweet_file = codecs.open(filename, encoding="utf-8")
    for line in tweet_file:
        tweet = json.loads(line).get('text')
        if tweet:
            words = tweet.strip().split()
            for word in words:
                if word.startswith('#'):
                    word = word[1:]
                    if word not in hashtag_occurrences:
                        hashtag_occurrences[word] = 1
                    else:
                        hashtag_occurrences[word] += 1
    tweet_file.close()

    sorted_hashtags = sorted(hashtag_occurrences.items(), key=lambda x: x[1], reverse=True)

    for hashtag, count in sorted_hashtags[:10]:
        print "%s %.1f" % (hashtag, count)


def main():
    print_top_ten_hashtag(sys.argv[1])


if __name__ == '__main__':
    main()


