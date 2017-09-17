import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer
import unicodedata
import re
import codecs
import pickle
import json

# verysmall full
# DATA_SIZE = 'verysmall'
DATA_SIZE = 'full'
# paths = {"verysmall":"data/",
paths = {"verysmall":"/scratch/ds222-2017/assignment-1/DBPedia.verysmall/",
        "full":"/scratch/ds222-2017/assignment-1/DBPedia.full/"}

dset_types = ['train', 'test', 'devel']

stopWords = set(stopwords.words('english'))
myStopWords = set(['(', ')','', ' ', '``', '@', '.', 'en', ',', '–', '[', ']'])
stopWords.update(myStopWords)
tokenizer = RegexpTokenizer(r'\w+')


if not os.path.isdir('data'):
    os.mkdir('data')

if not os.path.isdir('data/'+DATA_SIZE):
    os.mkdir('data/'+DATA_SIZE)

def readFile(path, dset_type):
    print("processing "+ dset_type + " data...")
    with codecs.open(path+DATA_SIZE+'_' + dset_type + '.txt', encoding='unicode_escape', errors='ignore') as f:
    # with open(path, encoding='ascii') as f:
        data = []
        count=0
        for line in f:
            # skip the first three lines
            # if count <3 and DATA_SIZE == 'verysmall':
            #     count += 1
            #     continue

            # For Debug
            # if count > 10:
            #     break
            # print(line)

            sents = line.split("\t")

            labels = sents[0].split(",")
            labels[-1] = labels[-1].strip()
            sentences = sents[1].split(" ", 2)

            # sentences = sentences[2].lower()

            tokens = []
            # sentences = sent_tokenize(sentences[2]);
            # for sentence in sentences:
                # tokens += [token for token in tokenizer.tokenize(sentence) if token not in stopWords]
            
            tokens = [token for token in sentences[2].split() if token not in stopWords]
            tokens = [token for token in sentences[2].split()]

            # print(tokens)
            data += [(labels, tokens)]
            count += 1
        # print(data)
        with open('data/' + DATA_SIZE + '/' + dset_type + '.json', "w") as f:
            json.dump(data, f)
        with open('data/' + DATA_SIZE + '/' + dset_type + '.pkl', "wb") as f:
            pickle.dump(data, f)

def write_all_data():
    for dset_type in dset_types:
        readFile(paths[DATA_SIZE], dset_type)

def get_train_data():
    with open('data/' + DATA_SIZE + '/' + 'train' + '.json', 'r') as  f:
        return pickle.load(f)

def get_data(d_size, dset_type):
    with open('data/' + d_size + '/' + dset_type + '.pkl', 'rb') as  f:
        return pickle.load(f)

if __name__ == "__main__":
    # readFile(paths[DATA_SIZE], 'train')
    write_all_data()
    # write_all_data()