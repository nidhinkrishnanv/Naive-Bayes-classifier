#!/usr/bin/env python3

import sys
import io

prev_word = None
current_count = 0
word = None

prev_lv_word = 'a'
len_vocab = 0

for line in sys.stdin:

    line = line.strip()

    # parse the input 
    word, value = line.split('\t', 1)

    # To get vocabulary length
    if value == 'len_vocab':
        if prev_lv_word != word:
            len_vocab += 1
            prev_lv_word = word
        continue

    count = int(value)

    if prev_word == word:
        current_count += count
    else:
        if prev_word:
            print('{}\t{}'.format(prev_word, current_count))
        prev_word = word
        current_count = count

# OUTPUT last word.
if prev_word == word:
    print('{}\t{}'.format(prev_word, current_count))

print("len_vocab\t{}".format(len_vocab))