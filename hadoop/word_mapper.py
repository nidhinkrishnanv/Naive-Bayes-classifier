#!/usr/bin/env python3

import sys

for line in sys.stdin:

    line = line.strip()

    # parse the input
    event, count = line.split('\t', 1)
    # count = int(count)

    if 'X=' in event:
        fields = event.split("^", 1)

        words = fields[1].split("=", 1)

        print(words[1] +'\t'+ count + "=w^" + fields[0])




