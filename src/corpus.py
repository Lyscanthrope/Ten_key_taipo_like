import numpy as np
import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data["characters"],data["bigrams"]

def build_frequency_vector(char_dict):
    return list(char_dict.keys()),list(char_dict.values())

def build_bigram_matrix(bigram_dict,chars):
    matrix = np.zeros((len(chars), len(chars)))
    for bigram in bigram_dict:
        char1,char2=bigram[0],bigram[1]
        index1,index2=chars.index(char1),chars.index(char2)
        matrix[index1][index2] = bigram_dict[bigram]
    return matrix

def get_matrix_from_json(path):
    chars,bigrams = load_json(path)
    list_char,list_freq=build_frequency_vector(chars)
    bigram_matrix=build_bigram_matrix(bigrams,list_char)
    return list_freq,bigram_matrix,list_char
