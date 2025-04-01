import numpy as np
import random
import matplotlib.pyplot as plt
from numba import njit
import numba as nb
import pickle

NUM_KEYS=8
def generate_ergonomic_chords(n_fingers=3):
    """Generate a list of all possible chords that are ergonomically friendly. This is a mtrix of all possible combinations by the number of keys)"""
    ergonomic_chords = []
    for i in range(1, 2**NUM_KEYS):  # Iterate through all possible chords
        finger_count = bin(i).count('1')  # Count fingers used
        if 1<=finger_count <= n_fingers : # Favor simpler chords
            ergonomic_chords.append(i)
    ergonomic_matrix=[]
    for chord in ergonomic_chords:
        ergonomic_matrix.append(np.array([c=='1' for c in bin(chord)[2:].zfill(NUM_KEYS)]))
    return np.array(ergonomic_matrix)

# Generate an initial random layout
def generate_random_layout(n_combination):
    """a layout is a correspondance table between the matrix and the characeter. it is a list of index."""
    list_of_index=list(range(n_combination))
    random.shuffle(list_of_index)
    return list_of_index


def plot_layout(layout,ergonomic_matrix,chars):
    """Plot the layout of a given list of chords"""
    #reorder the dictionnary
    reordered_chord=ergonomic_matrix.copy()
    # sorted_index=np.argsort(layout)
    reordered_chord=get_chords(layout,ergonomic_matrix,chars)
    plt.figure(figsize=(6,12))
    plt.imshow(reordered_chord,aspect="auto")
    plt.yticks(range(len(chars)),chars)
    plt.show()

def plot_layout_nicer(layout,ergonomic_matrix,chars):
    """Plot the layout of a given list of chords"""
    #reorder the dictionnary
    reordered_chord=ergonomic_matrix.copy()
    # sorted_index=np.argsort(layout)
    reordered_chord=get_chords(layout,ergonomic_matrix,chars)
    fig,ax=plt.subplots(len(reordered_chord)//4,4,figsize=(9,len(reordered_chord)/3))
    ax=ax.flatten()
    for i in range(len(reordered_chord)):
        ax[i].imshow(reordered_chord[i].reshape((2,4)),aspect="auto",cmap="Blues")
        ax[i].set_title(chars[i])
        ax[i].set_yticks([])
        ax[i].set_xticks([])
    plt.tight_layout()
    plt.show()


#@njit
def mutate(layout,mutation_rate,max_mutation=5):
    n_mut=random.randint(0,max_mutation)
    if random.random() < mutation_rate:
        for i in range(n_mut):
            # Pick a random character to mutate
            i1,i2=np.random.choice((len(layout)),2)
            layout[i1],layout[i2] = layout[i2],layout[i1] # Swap the two characters
    return layout

#@njit
def crossover(parent1, parent2):
    # Step 1: Take first half from parent1
    n_cut = random.randint(1, len(parent1) - 5) 
    if parent1==parent2:
        return parent1

    # index o remove
    random_index=np.random.choice(len(parent1), size=n_cut,replace=False)
    for r in random_index:
        parent1[r] = -1  # we mark the index to remove

    not_in_p1=[i for i in parent2 if i not in parent1]
    #we fill with the remaining index, in the same order
    for i,v in enumerate(parent1):
        if v==-1:
            parent1[i] = not_in_p1.pop(0)
 
    return parent1

def check_uniqueness_of_chords(layout):
    myset=set(layout)
    return len(myset)==len(layout)

def get_chords(layout,ergo_chords,chars):
    ordered_chords=ergo_chords[layout,:]
    ordered_chords=ordered_chords[:len(chars)]
    return ordered_chords

def save_keymaps(best_keymap,ergo_chords,chars):
    with open(r'./results/best_keymap.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([best_keymap,ergo_chords,chars], f)

def load_keymaps():
    with open(r'./results/best_keymap.pkl','rb') as f:  # Python 3: open(..., 'rb')
        best_keymap,ergo_chords,chars = pickle.load(f)
        return best_keymap,ergo_chords,chars