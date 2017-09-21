#!/usr/bin/env python3

import sys

prev_word = None
value_concat = ''

# input comes from STDIN
for line in sys.stdin:
    
    line = line.strip()

    word, value = line.split("\t", 1)

    
    if prev_word == word:
        # value_concat += " " + value
        value_concat += " " + value
    else:
        if prev_word:
            print("{}\t{}".format(prev_word, value_concat))
        value_concat = value
        prev_word = word

if prev_word == word:
    print("{}\t{}".format(prev_word, value_concat))