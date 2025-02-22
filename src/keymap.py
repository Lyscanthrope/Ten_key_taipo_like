import numpy as np
import random
import matplotlib.pyplot as plt
from numba import njit


NUM_KEYS=8
def generate_ergonomic_chords():
    """Generate a list of all possible chords that are ergonomically friendly. This is a list of matrixes of shape (2, 4)"""
    ergonomic_chords = []
    for i in range(1, 2**NUM_KEYS):  # Iterate through all possible chords
        finger_count = bin(i).count('1')  # Count fingers used
        if 1<=finger_count <= 3 : # Favor simpler chords
            ergonomic_chords.append(i)
    ergonomic_matrix=[]
    for chord in ergonomic_chords:
        ergonomic_matrix.append(np.array([c=='1' for c in bin(chord)[2:].zfill(NUM_KEYS)]).reshape((2,4)))
    return ergonomic_matrix

# Generate an initial random layout
def generate_random_layout(ergonomic_chords,list_chars):
    """list_chars is a list of characters that will be used to generate a random layout (a list of possible chords)"""
    random.shuffle(ergonomic_chords)
    list_chords=[]
    for i in range(len(list_chars)):
        list_chords.append(ergonomic_chords[i])
    return list_chords

def plot_layout(list_chords,list_chars):
    """Plot the layout of a given list of chords"""
    plt.figure()
    plt.imshow(np.concatenate(list_chords,axis=0),aspect="auto")
    plt.axis("off")
    plt.show()

@njit
def hashable_chord(chord=np.array([[]])):
    """Return the chord as a string"""
    return str(chord)


@njit
def mutate(layout, ergonomic_chords,mutation_rate):
    if random.random() < mutation_rate:
        # Pick a random character to mutate
        index_to_mutate = random.choice(range(len(layout)))
        #print("char to mutate: ", char_to_mutate, "layout: ",

        # Get all currently used chords
        used_chords = set()
        for chord in layout:
            used_chords.add(hashable_chord(chord))# Get all currently used chords in a hashable format

        # Find an unused ergonomic chord
        available_chords = [chord for chord in ergonomic_chords if hashable_chord(chord) not in used_chords]

        if available_chords:
            new_chord = random.choice(available_chords)  # Pick a random available chord
            layout[index_to_mutate] = new_chord  # Assign new chord

    return layout

@njit
def crossover(parent1, parent2):
    """a lot of fiddling with tuple of flattened array to allow to pass it into a set !"""
    # Step 1: Take first half from parent1
    child = [None]*len(parent1)
    assigned_chords = [hashable_chord(np.array([[]]))]#set(hashable_chord(np.array([[]])))
    assigned_chords=set()
    cut = random.randint(1, len(parent1) - 2) 

    random_index=np.random.choice(len(parent1), size=cut,replace=False)
    #random_index=random.sample(range(len(parent1)), cut)
    for r in random_index:
        child[r] = parent1[r]
        assigned_chords.add(hashable_chord(parent1[r]))
        # assigned_chords.append(hashable_chord(parent1[r]))


    # Step 2: Fill remaining characters from parent2, ensuring no duplicates
    for index in range(len(parent2)):
        if child[index] is None:
            if hashable_chord(parent2[index]) not in assigned_chords:
                child[index] = parent2[index]  # Directly assign if unused
                assigned_chords.add(hashable_chord(parent2[index]))
                # assigned_chords.append(hashable_chord(parent2[index]))
            else:
                # Step 3: Resolve conflicts by finding an available chord
                for chord in parent1:
                    if hashable_chord(chord) not in assigned_chords:
                        child[index] = chord
                        assigned_chords.add(hashable_chord(chord))
                        # assigned_chords.append(hashable_chord(chord))
                        break

    return child

def check_uniqueness_of_chords(layout):
    myset=set()
    for l in layout:
        myset.add(hashable_chord(l))
    return len(myset)==len(layout)