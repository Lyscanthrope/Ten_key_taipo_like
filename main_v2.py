import random
import matplotlib.pyplot as plt
from tqdm import tqdm
from numba import jit,njit
from numba.typed import Dict

# Define the 10-key structure: 8 fingers + 2 thumbs
NUM_KEYS = 10
POP_SIZE =200  # Population size for genetic algorithm
GENS = 500  # Number of generations
MUTATION_RATE = 0.5  # Probability of mutation

# Frequency of characters (normalized)
char_freq={
		"e": 0.14165751413797095,
		"s": 0.07820867962743913,
		"a": 0.07250352759782898,
		"n": 0.070452733981691,
		"i": 0.0688537625858721,
		"t": 0.06698185216891259,
		"r": 0.06587441317373717,
		"o": 0.05416638686637213,
		"u": 0.05411432190944767,
		"l": 0.05270941692283689,
		"d": 0.038616242854585967,
		"c": 0.033956531712530144,
		"p": 0.028925043336533084,
		"m": 0.02632033803027537,
		"é": 0.023621138062440716,
		"v": 0.013626956627283469,
		"'": 0.012634708226174785,
		".": 0.012261249307578355,
		"f": 0.010743796374216132,
		"g": 0.01014862415068038,
		",": 0.0100881411608534,
		"b": 0.008811111475422732,
		"q": 0.008162874893796008,
		"h": 0.007927961165115717,
		"à": 0.004296835625556005,
        "è": 0.004296835625556005,
		"x": 0.003978017043813119,
		"j": 0.003759023263201894,
		"y": 0.0027040143907617817,
		"z": 0.0012336486277446806,
		"k": 0.0011269593500110068,
		"w": 0.000591065709768238}
bigram_freq = {
    ('l', 'e'): 0.026, ('e', 'n'): 0.0245, ('e', 's'): 0.0243, ('d', 'e'): 0.0231, ('r', 'e'): 0.0206,
    ('a', 'i'): 0.0194, ('o', 'u'): 0.0192, ('n', 't'): 0.0187, ('o', 'n'): 0.0169, ('e', 'r'): 0.0140,
    ('u', 'r'): 0.0138, ('a', 'n'): 0.0133, ('i', 't'): 0.0133, ('t', 'e'): 0.0129, ('e', 't'): 0.0128,
    ('m', 'e'): 0.0123, ('l', 'a'): 0.0123, ('i', 's'): 0.0122, ('q', 'u'): 0.0115, ('s', 'e'): 0.0103,
    ('i', 'l'): 0.0100, ('u', 'e'): 0.0098, ('u', 's'): 0.0097, ('e', 'u'): 0.0095, ('c', 'o'): 0.0095,
    ('r', 'a'): 0.0092, ('n', 'e'): 0.0091, ('i', 'n'): 0.0089, ('v', 'e'): 0.0088, ('p', 'a'): 0.0087,
    ('m', 'a'): 0.0087, ('a', 'u'): 0.0087, ('a', 'r'): 0.0084, ('n', 's'): 0.0082, ('c', 'h'): 0.0082,
    ('i', 'e'): 0.0081, ('t', 'i'): 0.0080, ('t', 'r'): 0.0079, ('c', 'e'): 0.0078, ('e', 'm'): 0.0077,
    ('u', 'n'): 0.0076
}


# Generate ergonomic chords: 1-3 fingers + at most 1 thumb
def generate_ergonomic_chords():
    ergonomic_chords = []
    for i in range(1, 2**NUM_KEYS):  # Iterate through all possible chords
        finger_count = bin(i & 0xFF).count('1')  # Count fingers used
        thumb_count = bin((i & 0x300) >> 8).count('1')  # Count thumbs used
        if 1 <= finger_count <= 3 and thumb_count <= 0:  # Favor simpler chords
            ergonomic_chords.append(i)
    return ergonomic_chords

# Generate an initial random layout
def generate_random_layout(ergonomic_chords):
    random.shuffle(ergonomic_chords)
    d = Dict()
    for i, char in enumerate(char_freq.keys()):
        d[char] = ergonomic_chords[i]

    # return {char: ergonomic_chords[i] for i, char in enumerate(char_freq.keys())}
    return d


def layout_cost(layout, char_freq=char_freq, bigram_freq=bigram_freq):
    total_cost = 0
    # penalization of same finger on both level
    index=0b0000010001
    majeur=0b0000100010
    annulaire=majeur=0b0001000100
    auriculaire=0b0010001000
    list_same_finger = [index,majeur,annulaire,auriculaire]
    for char, chord in layout.items():
        press_count = bin(chord).count('1')*1  # How many keys are pressed
        effort = press_count  # Penalize more fingers pressed
        total_cost += (effort * char_freq.get(char, 0))
        for i,same in enumerate(list_same_finger) :
            finger_cost = 0.01*max(i-1,0)
            finger_count=bin(chord & same).count('1')
            if finger_count ==2 :
                total_cost+=0.5# this is for penalizing the vertical combo
            if finger_count ==1 :
                total_cost+=finger_cost# this is for positions (more on stronger fingers)

            
    for (char1, char2), freq in bigram_freq.items():
        if char1 in layout and char2 in layout:
            chord1, chord2 = layout[char1], layout[char2]
            transition_cost = bin(chord1 ^ chord2).count('1')  # Key changes between chords
            total_cost += 0.1*(transition_cost * freq)
    return total_cost


# Crossover: Combines two parent layouts
def crossover(parent1, parent2):
    # Step 1: Take first half from parent1
    child = {}
    assigned_chords = set()
    cut = random.randint(1, len(parent1) - 2) 

    random_keys=random.sample(list(parent1.keys()), cut)
    for r in random_keys:
        child[r] = parent1[r]
        assigned_chords.add(parent1[r])


    # Step 2: Fill remaining characters from parent2, ensuring no duplicates
    for char in parent2.keys():
        if char not in child:
            if parent2[char] not in assigned_chords:
                child[char] = parent2[char]  # Directly assign if unused
                assigned_chords.add(parent2[char])
            else:
                # Step 3: Resolve conflicts by finding an available chord
                for chord in parent1.values():
                    if chord not in assigned_chords:
                        child[char] = chord
                        assigned_chords.add(chord)
                        break

    return child


def mutate(layout, ergonomic_chords):
    if random.random() < MUTATION_RATE:
        # Pick a random character to mutate
        char_to_mutate = random.choice(list(layout.keys()))

        # Get all currently used chords
        used_chords = set(layout.values())

        # Find an unused ergonomic chord
        available_chords = [chord for chord in ergonomic_chords if chord not in used_chords]

        if available_chords:
            new_chord = random.choice(available_chords)  # Pick a random available chord
            layout[char_to_mutate] = new_chord  # Assign new chord

    return layout


# Genetic Algorithm
def genetic_algorithm():
    best_score = []
    ergonomic_chords = generate_ergonomic_chords()
    print(len(ergonomic_chords))
    population = [generate_random_layout(ergonomic_chords) for _ in range(POP_SIZE)]
    progress=tqdm(range(GENS))
    for _ in progress:
        population = sorted(population, key=layout_cost) 
        progress.set_description(str(layout_cost(population[0])))
        
         # Rank by cost
        best_score.append(layout_cost(population[0]))
        next_gen = population[:POP_SIZE // 2]  # Keep best 50%
        
        while len(next_gen) < POP_SIZE:
            p1, p2 = random.sample(population[:POP_SIZE // 4], 2)  # Select top candidates
            child = crossover(p1, p2)
            child = mutate(child, ergonomic_chords)
            next_gen.append(child)
        
        population = next_gen  # Move to next generation
    
    return sorted(population, key=layout_cost)[0],best_score  # Best layout

# Run optimization
best_layout,best_score = genetic_algorithm()

# Print result
print("\nOptimized 10-Key Chording Layout:")
for char, chord in best_layout.items():
    print(f"Character: {char}, Chord: {bin(chord)[2:].zfill(NUM_KEYS)}")

# plt.plot(best_score)
# plt.show()
