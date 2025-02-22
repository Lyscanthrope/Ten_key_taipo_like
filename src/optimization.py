
def layout_cost(layout, char_freq, bigram_freq):
    total_cost = 0

    for i,chord in enumerate(layout):
        press_count = chord.sum()  # How many keys are pressed
        effort = press_count  # Penalize more fingers pressed
        total_cost += (effort * char_freq[i])
            
    # for (char1, char2), freq in range(bigram_freq.items():
    #     if char1 in layout and char2 in layout:
    #         chord1, chord2 = layout[char1], layout[char2]
    #         transition_cost = bin(chord1 ^ chord2).count('1')  # Key changes between chords
    #         total_cost += 0.1*(transition_cost * freq)
    return total_cost
