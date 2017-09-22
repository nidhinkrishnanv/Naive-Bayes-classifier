#!/usr/bin/env python3

import sys

prev_word = None
value_list = []

for line in sys.stdin:

    # Remove space and new line
    line = line.strip()
    # print(line)

    # Get word and its value
    word, value = line.split("\t", 1)
    # print("{}\t{}".format(word, value))

    if prev_word == word:
        value_list.append(value)
    else:
        if prev_word:
            sorted_value = sorted(value_list)
            if "=w^Y=" in sorted_value[0]:
                for i in range(1, len(sorted_value)):
                    _, Id = sorted_value[i].split()
                    print("{}\t~ctr_for {} {}".format(Id, prev_word, sorted_value[0]))
        value_list = [value]
        prev_word = word

if prev_word == word:
    sorted_value = sorted(value_list)
    if "=w^Y=" in sorted_value[0]:
        for i in range(1, len(sorted_value)):
            _, Id = sorted_value[i].split()
            print("{}\t~ctr_for {} {}".format(Id, prev_word, sorted_value[0]))

