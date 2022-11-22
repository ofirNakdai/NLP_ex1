import json
import pickle
import os.path
from collections import defaultdict
from matplotlib import pyplot as plt
from math import log
import seaborn as sn
sn.set()


def read_data(filename):
    word2freq = defaultdict(int)

    with open(filename, 'r', encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                word2freq[word] += 1
            if i % 100000 == 0:
                print(i)

    total_words = sum(word2freq.values())
    word2nfreq = {w: word2freq[w]/total_words for w in word2freq}

    return word2nfreq


def test_zipf_law(word2nfreq):
    y = sorted(word2nfreq.values(), reverse=True)
    x = list(range(1, len(y)+1))

    product = [a * b for a, b in zip(x, y)]
    print(product[:1000])  # todo: print and note the roughly constant value

    y = [log(e, 2) for e in y]
    x = [log(e, 2) for e in x]

    plt.plot(x, y)
    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title("Zipf's law")
    plt.show()
    
    
def read_data_heaps(filename):
    word2freq = defaultdict(int)
    data = defaultdict(int)
    total_counter = 0
    unique_counter = 0

    with open(filename, 'r', encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                word2freq[word] += 1
                if(word2freq[word] == 1):
                    unique_counter += 1
                total_counter += 1
            if i % 500000 == 0:
               data[total_counter] = unique_counter
               print(i) 

    return data

def  Heaps_law(data):
    x = data.keys()
    y = data.values()
    
    plt.plot(x, y)
    plt.xlabel('Num of tokens')
    plt.ylabel('Num of types')
    plt.title("Heap's law")
    plt.show()
    
    


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    #if not os.path.isfile('word2nfreq.pkl'):
    #    data = read_data(config['corpus'])
    #    pickle.dump(data, open('word2nfreq.pkl', 'wb'))

    if not os.path.isfile('uniqueCounter.pkl'):
        data = read_data_heaps(config['corpus'])
        pickle.dump(data , open('uniqueCounter.pkl', 'wb'))
        
    #test_zipf_law(pickle.load(open('word2nfreq.pkl', 'rb')))
    Heaps_law(pickle.load(open('uniqueCounter.pkl', 'rb')))

