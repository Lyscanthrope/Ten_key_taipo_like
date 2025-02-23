import numpy as np
from src import keymap
from numba import njit

homerow_coef=0.9
relative_weighting=np.array([1.4,1.2,1.,1.,1.4*homerow_coef,1.2*homerow_coef,1.*homerow_coef,1.*homerow_coef])
index=[0,0,0,1]*2
majeur=[0,0,1,0]*2
annulaire=[0,1,0,0]*2
auriculaire=[1,0,0,0,]*2
list_same_finger = np.vstack([index,majeur,annulaire,auriculaire])

tab=[0,1,1,1,0,0,0,0]
enter=[0,0,0,0,0,1,1,1]
list_prohibited=np.vstack([tab,enter])

def get_bigram_cost(ordered_chords, char_freqs,bigram_freq):
    #a bit slow but it works
    bigram_cost=0
    n_chars = len(char_freqs)
    list_i,list_j=np.where(bigram_freq>0)
    for index in range(len(list_i)):
        i=list_i[index]
        j=list_j[index]
        i1=ordered_chords[i]
        i2=ordered_chords[j]
        n_finger=np.array((i1^i2))@list_same_finger.T
        bigram_cost+=float(2*sum(n_finger>=2)*bigram_freq[i][j])**2
    return bigram_cost

def layout_cost(layout, char_freqs, bigram_freq,ergo_chords):
    total_cost = 0
    ordered_chords=keymap.get_chords(layout,ergo_chords,char_freqs)
    
    # to get more frequent keys with less fingers
    total_finger_press=np.sum(((ordered_chords*relative_weighting).sum(axis=1)*char_freqs)**2)
    
    #to prevent same fingers from being used in the same column
    same_col_chords=(ordered_chords@list_same_finger.T>1).sum()

    # to make bigram easily one need not to move the finger to a different row
    bigram_cost=get_bigram_cost(ordered_chords, char_freqs,bigram_freq)

    #prohibited chord cost
    prohibited_chords=(ordered_chords@list_prohibited.T>2).sum()

    total_cost+=total_finger_press
    total_cost+=same_col_chords*5
    total_cost+=bigram_cost

    total_cost+=prohibited_chords*5
    return total_cost
