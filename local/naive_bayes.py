from process_data import get_data, DATA_SIZE, readFile, paths
import os
import json
import math
import operator
import time

if not os.path.isdir('models'):
    os.mkdir('models')

def train():

    print("Training")
    
    since = time.time()

    data = readFile(paths[DATA_SIZE], 'train')

    
    # Data structure to store parameters
    total_label_count = 0   # C(Y=ANY)
    label_count = {}        # C(Y=label)++
    label_word_count = {}    # Y=y and X=x
    label_any_word_count = {}  # Y=y and X=ANY
    vocab = set()
    dom_labels = set()


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

    time_elapsed = time.time() - since
    print("Time for training {}".format(time_elapsed))

    naive_bayes_data = {'total_label_count' : total_label_count,
                        'label_count' : label_count,
                        'label_word_count' : label_word_count,
                        'label_any_word_count' : label_any_word_count,
                        'len_vocab' : len(vocab),
                        'dom_labels' : list(dom_labels)}

    with open('models/naive_bayes_data.json', 'w') as f:
        json.dump(naive_bayes_data, f)

    print()

    return naive_bayes_data
    

def get_model():
    with open('models/naive_bayes_data.json', 'r') as f:
        return json.load(f)

def devel(nb=None, m=1):
    
    if not nb:
        nb = get_model()

    print("Validating ")

    since = time.time()

    data = readFile(paths[DATA_SIZE], 'devel')

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
    time_elapsed = time.time() - since


    print("Time for Validating {}".format(time_elapsed))
    print("Accuracy {:.4f}".format(correct/len(data)))
    
    print()
    return correct/len(data)


def test(nb=None, m=1):
    if not nb:
        nb = get_model()


    print("Testing  ")

    since = time.time()

    data = readFile(paths[DATA_SIZE], 'test')

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

    time_elapsed = time.time() - since

    print("Time for Testing {}".format(time_elapsed))

    print("Accuracy {:.4f}".format(correct/len(data)))
    print()


def count_param():
    nb = get_model()
    total_label_count = nb['total_label_count']
    label_count = nb['label_count']

    label_word_count = nb['label_word_count'] 
    label_any_word_count = nb['label_any_word_count']

    len_v = nb['len_vocab']
    dom_labels = nb['dom_labels']

    total_param_c = 1

    label_count_param_c = len(label_count)
    total_param_c += label_count_param_c

    label_word_count_param_c = 0
    
    for label in label_any_word_count:
        label_word_count_param_c += len(label_word_count[label])
    total_param_c += label_word_count_param_c

    label_any_word_count_param_c = len(label_any_word_count)
    total_param_c += label_any_word_count_param_c


    dom_labels_param_c = len(dom_labels)

    print("Param count for C(Y=label) " + str(label_count_param_c))
    print("Param count for Y=y and X=x " + str(label_word_count_param_c))
    print("Param count for Y=y and X=ANY " + str(label_any_word_count_param_c))
    print("Number of dom labels " +str(dom_labels_param_c))
    print("Total param count " + str(total_param_c))
    print('total_label_count ' + str(total_label_count))

if __name__ == "__main__":
    
    nb = train()

    # best_acc = 0
    # m_vals = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
    # m_vals = [0.0001, 0.001, 0.01]
    # for m in m_vals:
    #     acc = devel(m)
    #     if best_acc < acc:
    #         best_acc = acc
    # print("Best acc : {:.5f}\n".format(best_acc))

    # test(nb, 0.0001)

    devel(nb, 1)

    test(nb, 1)

    count_param()