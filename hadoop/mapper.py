#!/usr/bin/env python3

import sys

stopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'])
myStopWords = set(['(', ')','', ' ', '``', '@', '.', 'en', ',', '–', '[', ']'])
stopWords.update(myStopWords)

# input comes from STDIN (standard input)
vocab = set()
for line in sys.stdin:

    # Split into labels and sentence
    fields = line.split('\t')

    labels = fields[0].split(",")
    labels[-1] = labels[-1].strip()

    # Split the training data to remove the links
    fields = fields[1].split(" ", 2)

    line = fields[2].strip()
    
    # Split the line into words
    words = line.split()
    words[0] = words[0].strip("\"")
    words[-2] = words[-2].strip("\"@en")

    for label in labels:
        print('Y=ANY\t{}'.format(1))
        print('Y={}\t{}'.format(label, 1))
        for word in words:
            if word not in stopWords:
                vocab.add(word)
                print('Y={} ^ X={}\t{}'.format(label, word, 1))
                print('Y={} ^ X=ANY\t{}'.format(label, 1))
            # print('%s\t%s' % (word, 1))

print('len_vocab\t{}'.format(len(vocab)))