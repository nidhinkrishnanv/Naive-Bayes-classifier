#!/usr/bin/env python3

import sys
import math

prev_Id = None
value_list = []

stopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'])
myStopWords = set(['(', ')','', ' ', '``', '@', '.', 'en', ',', '–', '[', ']'])
stopWords.update(myStopWords)

# Data structure to store parameters
total_label_count = 0   # C(Y=ANY)
label_count = {}        # C(Y=label)++
len_vocab = 0
line_count = 0
label_any_word_count = {}  # Y=y and X=ANY
dom_size = 0
label_word_count = {}

# label_word_count = {}    # Y=y and X=x
# vocab = set()
# dom_labels = set()

# Process cache
for line in open('cf'):
    line.strip()

    key, value = line.split("\t", 1)

    # C(Y=ANY)
    if key == "Y=ANY":
        total_label_count = int(value)
        continue

    if key == 'len_vocab':
        len_vocab = int(value)
        continue

    if key == 'line_count':
        line_count = int(value)
        continue

    # C(Y=label)++
    if "X=" not in key:
         _,label = key.split("=",1)
         label_count[label] = int(value)
         continue

    # Y=y and X=ANY
    label, _ = key.split("^", 1)
    _,label = label.split("=", 1)
    label_any_word_count[label] = int(value)

dom_size = len(label_count)

# print(total_label_count)
# print(label_count)
# print(label_any_word_count)

num_correct = 0
num_doc = 0

m=1
q_x = 1/len_vocab
q_y = 1/dom_size

for line in sys.stdin:

    # print(line)

    line = line.strip()

    Id, value = line.split("\t", 1)

    if prev_Id == Id:
        value_list.append(value)
    else:
        if prev_Id:
            sorted_value = sorted(value_list)

            # print(sorted_value)

            # Get the ground truths
            _, labels = sorted_value[0].split(" ", 1)
            labels = labels.split(",")
            labels[-1] = labels[-1].strip()

            sentence = sorted_value[1].split()
            sentence[0] = sentence[0].strip("\"")
            sentence[-2] = sentence[-2].strip("\"@en")

            words = [x for x in sentence if x not in stopWords]

            prob_y = {}

            label_word_count = {}
            for i in range(2, len(sorted_value)):
                # Ignore ~ctr_for and get word and count label list
                _, word, counts = sorted_value[i].split(" ", 2)

                # print(counts)
                for count_label in counts.split():

                    # Get the count and label.
                    count, _, label = count_label.split("=", 2)

                    if label not in label_word_count:
                        label_word_count[label] ={}

                    label_word_count[label][word] = int(count)

            for label in label_count:
                prob_y[label] = math.log( (label_count[label]+m*q_y) / (total_label_count+m) )
                for word in words:
                    if label in label_word_count and word in label_word_count[label]:
                        num = label_word_count[label][word] + m*q_x
                    else:
                        num = m*q_x
                    den = label_any_word_count[label] + m
                    prob_y[label] += math.log(num/den)

            max_label = max(prob_y, key=prob_y.get)

            if max_label in labels:
                num_correct += 1

            print("{}\t{}".format(prev_Id, max_label))
            print("{}\tGroud truth : {}".format(prev_Id, labels))

        value_list = [value]
        prev_Id = Id
        num_doc += 1

print("Stats\t{} {}".format(num_correct, num_doc))


            # for label in label_count:
            #     prob_y[label] = math.log((label_count[label]+m*q_y)/(total_label_count+m))

            # for i in range(2, len(sorted_value)):
            #     # Ignore ~ctr_for and get word and count label list
            #     _, word, counts = sorted_value[i].split(" ", 2)

            #     if word in words_set:
            #         words_set.remove(word)

            #     # print(counts)
            #     for count_label in counts.split():

            #         # Get the count and label.
            #         count, _, label = count_label.split("=", 2)

            #         # Calculate prob for label.
            #         num = int(count) + m*q_x
            #         den = label_any_word_count[label] + m

            #         prob_y[label] += math.log(num/den)