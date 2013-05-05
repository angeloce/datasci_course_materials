#coding:utf-8

import sys


def hw():
    print 'Hello, world!'


def lines(fp):
    print str(len(fp.readlines()))


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    for line in sent_file:
        sd = line.split()
        if len(sd) > 2:
            print line

    hw()
    lines(sent_file)
    lines(tweet_file)


if __name__ == '__main__':
    sys.argv.append('AFINN-111.txt')
    sys.argv.append('head_20_output.txt')
    main()
