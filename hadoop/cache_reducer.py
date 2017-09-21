#!/usr/bin/env python3

import sys

len_vocab = 0
flag = False

for line in sys.stdin:
    line = line.strip()
    
    key, value = line.split("\t", 1)

    if key == 'len_vocab':
        len_vocab += int(value)
        flag = True

    if key == 'line_count':
        print(line)


    if "X=ANY" in key:
        print(line)

    if "Y=" in key and "X=" not in key:
        print(line)

if flag:
    print("len_vocab\t{}".format(len_vocab))