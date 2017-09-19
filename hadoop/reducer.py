#!/usr/bin/env python3

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    count = int(count)
    # # convert count (currently a string) to int
    # try:
    #     count = int(count)
    # except ValueError:
    #     # count was not a number, so silently
    #     # ignore/discard this line
    #     continue

    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            # print '%s\t%s' % (current_word, current_count)
            print('{}\t{}'.format(current_word, current_count))

        current_count = count
        current_word = word

# OUTPUT last word.
if current_word == word:
    print('{}\t{}'.format(current_word, current_count))
    # print '%s\t%s' % (current_word, current_count)