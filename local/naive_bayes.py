from process_data import get_data, DATA_SIZE
import os
import json
import math
import operator
import time

# verysmall full
# DATA_SIZE = 'verysmall'
# DATA_SIZE = 'full'

if not os.path.isdir('models'):
    os.mkdir('models')

def train():
    since = time.time()
    data = get_data(DATA_SIZE, 'train')
    # print(data)
    total_label_count = 0   # C(Y=ANY)
    label_count = {}        # C(Y=label)++
    label_word_count = {}    # Y=y and X=x
    label_any_word_count = {}  # Y=y and X=ANY
    vocab = set()
    dom_labels = set()

    print("Training on data of size ", len(data))

    for labels, words in data:
        
        for label in labels:
            dom_labels.add(label)
            total_label_count +=1   # C(Y=ANY)
            if label not in label_count:    # C(Y=label)++
                label_count[label] = 0
                label_word_count[label] = {}
                label_any_word_count[label] = 0
            label_count[label] += 1

            for word in words:
                # C(Y=labe AND X=word)
                vocab.add(word)
                word_count = 0
                if word in label_word_count[label]:
                    word_count = label_word_count[label][word]
                word_count += 1
                label_word_count[label][word] = word_count

                label_any_word_count[label] += 1    # C(Y=label AND X=ANY)

    naive_bayes_data = {'total_label_count' : total_label_count,
                        'label_count' : label_count,
                        'label_word_count' : label_word_count,
                        'label_any_word_count' : label_any_word_count,
                        'len_vocab' : len(vocab),
                        'dom_labels' : list(dom_labels)}

    with open('models/naive_bayes_data.json', 'w') as f:
        json.dump(naive_bayes_data, f)

    time_elapsed = time.time() - since
    print("Time for training {}".format(time_elapsed))
    print()

def get_model():
    with open('models/naive_bayes_data.json', 'r') as f:
        return json.load(f)

def devel(m):
    since = time.time()
    nb = get_model()

    correct = 0;
    prob_y = {}
    # m = 1

    total_label_count = nb['total_label_count']
    label_count = nb['label_count']

    label_word_count = nb['label_word_count'] 
    label_any_word_count = nb['label_any_word_count']

    len_v = nb['len_vocab']
    dom_labels = nb['dom_labels']

    q_x = 1 / len_v
    q_y = 1 / len(dom_labels)


    data = get_data(DATA_SIZE, 'devel')

    print("Validating on data of size ", len(data))
    print("Current m {} value".format(m))
    # print(data[:4])
    for labels, words in data:
        for label in dom_labels:
            prob_y[label] = math.log( (label_count[label]+m*q_y) / (total_label_count+m) )
            for word in words:
                if word in label_word_count[label]:
                    num = label_word_count[label][word] + m*q_x
                else:
                    num = m*q_x
                den = label_any_word_count[label] + m
                prob_y[label] += math.log(num/den)
        max_label = max(prob_y, key=prob_y.get)

        if max_label in labels:
            correct +=1

    print(correct)
    # print(len(data))
    print("Accuracy {:.4f}".format(correct/len(data)))
    time_elapsed = time.time() - since
    print("Time for training {}".format(time_elapsed))
    print()
    return correct/len(data)


def test(m=1):
    since = time.time()
    nb = get_model()

    correct = 0;
    prob_y = {}
    # m = 1

    total_label_count = nb['total_label_count']
    label_count = nb['label_count']

    label_word_count = nb['label_word_count'] 
    label_any_word_count = nb['label_any_word_count']

    len_v = nb['len_vocab']
    dom_labels = nb['dom_labels']

    q_x = 1 / len_v
    q_y = 1 / len(dom_labels)


    data = get_data(DATA_SIZE, 'test')

    print("Testing on data of size ", len(data))

    for labels, words in data:
        for label in dom_labels:
            prob_y[label] = math.log( (label_count[label]+m*q_y) / (total_label_count+m) )
            for word in words:
                if word in label_word_count[label]:
                    num = label_word_count[label][word] + m*q_x
                else:
                    num = m*q_x
                den = label_any_word_count[label] + m
                prob_y[label] += math.log(num/den)
        max_label = max(prob_y, key=prob_y.get)

        if max_label in labels:
            correct +=1
    print(correct)
    # print(len(data))
    print("Accuracy {:.4f}".format(correct/len(data)))
    time_elapsed = time.time() - since
    print("Time for Testing {}".format(time_elapsed))
    print()




if __name__ == "__main__":
    
    train()

    best_acc = 0
    # m_vals = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
    # m_vals = [0.0001, 0.001, 0.01]
    # for m in m_vals:
    #     acc = devel(m)
    #     if best_acc < acc:
    #         best_acc = acc
    # print("Best acc : {:.5f}\n".format(best_acc))

    # test(0.0001)

    test(1)