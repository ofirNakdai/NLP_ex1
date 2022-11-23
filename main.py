import json
from collections import defaultdict

def count_word_in_corpus(corpus, word1):
    counter = 0
    with open(corpus, 'r', encoding='utf-8') as fin:
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                if word == word1:
                    counter += 1
    return counter

def count_couple_in_corpus(corpus, word1, word2):
    counter = 0
    with open(corpus, 'r', encoding='utf-8') as fin:
        for i, line in enumerate(fin.readlines()):
            words_list = line.split()
            for word in words_list:
                j = words_list.index(word)
                if word == word1 and j > words_list.__len__() and words_list[j+1] == word2:
                    counter +=1
    return counter


def calc_prob(corpus, left, candidate, right):
    prob1 = prob2 = 1
    
    if left != "<S>":
        prob1 = count_couple_in_corpus(corpus,left,candidate) / count_word_in_corpus(corpus, left)
    if right != "<S>":
        prob2 = count_couple_in_corpus(corpus,candidate,right) / count_word_in_corpus(corpus, candidate)
    return (prob1 * prob2)

def get_candidates():# todo
    return 0


def find_best_candid(corpus, left, right, candidates_list):
    prob_dict = defaultdict()
    
    for cand in candidates_list:
        prob_dict[calc_prob(corpus, left, cand, right)] = cand
    
    return prob_dict[max(prob_dict.keys)]
    
    
    


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    reslist = []
    candid_list = get_candidates(candidates)
    left = right = ""
       
    with open(input, 'r', encoding='utf-8') as fin:
        
        for i, line in enumerate(fin.readlines()):
            line_to_words_list = line.split()
            if "__________" in line_to_words_list:
                for word in line_to_words_list:
                    if word == "__________":
                        j = line_to_words_list.index(word)
                        if j == 0: #beginning of line
                            if j + 1 == line_to_words_list._len_(): #end of line
                                left = right = "<s>"
                            else:
                                left = "<s>"
                                right = line_to_words_list[j+1]
                        else:
                            if j + 1 == line_to_words_list._len_():#end of line
                                left = line_to_words_list[j-1]
                                right = "<s>"
                            else:
                                left = line_to_words_list[j-1]
                                right = line_to_words_list[j+1]
                    
                    chosen_candid = find_best_candid(corpus, left, right, candid_list)
                    reslist.append(chosen_candid)
                    #todo: remove chosen_candid from candid_list
                            
                
    
    
    return list()  # return your solution


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
