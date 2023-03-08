import itertools
import string

letter_frequencies = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
    'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
    'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.01974, 'Z': 0.00074
}

keys = string.ascii_uppercase  # dictionary keys

# generate all possible value combinations
values = []

# Define the dice types and their corresponding number of sides
dice_types = {'D2': 2, 'D4': 4, 'D6': 6, 'D8': 8, 'D10': 10}

# Define the method for selecting the letter from the book
letter_selection_method = 'first letter of the last word on the page'


def calculate_probability(f, d, n):
    p = [0] * n

    for letter, freq in f.items():
        for i in range(1, n + 1):
            if d.get(letter, 0) == i:
                p[i - 1] += freq

    return p


weight_best = 1
pips_distribution_best = {'D2': {}, 'D4': {}, 'D6': {}, 'D8': {}, 'D10': {}}


# Loop over each dice type
for dice_type in dice_types.keys():
    for combination in itertools.product(list(range(1, dice_types[dice_type]+1)), repeat=len(keys)):
        pips_distribution = {key: value for key, value in zip(keys, combination)}
        # print(combination)
        total_probability = calculate_probability(letter_frequencies, pips_distribution, dice_types[dice_type])
        weight = sum([(p-1/dice_types[dice_type])**2 if letter_frequencies[list(letter_frequencies)[i]] <= 1/dice_types[dice_type] else 0 for i, p in enumerate(total_probability)])
        if weight < weight_best:
            weight_best = weight
            pips_distribution_best[dice_type] = {key: (None if letter_frequencies[key] >= 1 / dice_types[dice_type] else value) for key, value in pips_distribution.items()}
        else:
            pass


print(pips_distribution_best)
