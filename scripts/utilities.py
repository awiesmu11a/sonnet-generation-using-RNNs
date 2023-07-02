import string
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import time

def poem_info(path, space, split_hyphen):

    with open(path, 'r') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
    
    raw_data = data
    data = [line for line in data if line != '']
    data = [word for word in data if not word.isdigit()]

    avg_char_len = np.floor(np.mean([len(line) for line in data if line != '']))

    max_word_len = 0

    for sentence in data:
        sentence_len = 0
        for word in sentence:
            if split_hyphen:
                if word == '-':
                    sentence_len += 2
                    continue
            if word == ' ':
                if space:
                    sentence_len += 2
                else:
                    sentence_len += 1
            if word == "." or word == "," or word == ";" or word == ":" or word == "?" or word == "!":
                sentence_len += 1
        sentence_len += 1
        if sentence_len > max_word_len:
            max_word_len = sentence_len

    return raw_data, data, avg_char_len, max_word_len

def word_tokenized_input(raw_data, sequence, split_hyphen, max_word_len, space):
    data = raw_data
    data = [line for line in data if line != '']
    data = [word for word in data if not word.isdigit()]
    
    word_list = []

    for sentence in data:
        words = sentence.split()
        line = []
        for i in range(len(words)):
            if split_hyphen:
                temp = words[i].split('-')
                for j in range(len(temp)):
                    line.append(temp[j])
                    if j < len(temp) - 1:
                        line.append('-')
            else:
                line.append(words[i])
            if i < len(words) - 1 and space:
                line.append(' ')  

        word_list.append(line)

    # Now seperating the punctuations from the end of the words
    for i in range(len(word_list)):
        for j in range(len(word_list[i])):
            if word_list[i][j][-1] in string.punctuation:
                punctuations = word_list[i][j][-1]
                word_list[i][j] = word_list[i][j][:-1]
                word_list[i].insert(j+1, punctuations)

    data = []
    for i in range(len(word_list)):
        temp = []
        for j in range(max_word_len):
            if j < len(word_list[i]):
                temp.append(word_list[i][j])
            else:
                temp.append('0')
        data.append(temp)
    
    for i in range(len(data)):
        if (i+1) % 14 == 0:
            data[i].append('|')
            continue
        if (i+1) % 14 == 12 or (i+1) % 14 == 8 or (i+1) % 14 == 4:
            data[i].append('&')
            continue
        else:
            data[i].append('~')
        
    word_list = []

    for i in range(0, len(data)):
        temp = []
        if i + sequence >= len(data):
            break
        for j in range(sequence):
            temp.append(data[i+j])
        word_list.append(temp)
    
    data = []
    for i in range(len(word_list)):
        temp = []
        for j in range(sequence):
            temp = temp + word_list[i][j]
        data.append(temp)
    
    data = np.array(data)
    data = np.char.lower(data)

    return data