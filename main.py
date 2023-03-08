import string
import pprint as pp
import itertools

# Define the letter frequencies in the English language
letter_frequencies = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
    'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
    'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.01974, 'Z': 0.00074
}

# Define the dice types and their corresponding number of sides
dice_types = {'D2': 2, 'D4': 4, 'D6': 6, 'D8': 8, 'D10': 10}

# Define the method for selecting the letter from the book
letter_selection_method = 'first letter of the last word on the page'

# Initialize an empty dictionary to hold the rows of the table
table = {}


def calculate_probability(f, d, N):
    total_probability = [0] * N

    for letter, freq in f.items():
        for i in range(1, N + 1):
            if d.get(letter, 0) == i:
                total_probability[i - 1] += freq

    return total_probability


# Loop over each dice type
for dice_type in dice_types.keys():
    # Initialize a list to hold the numbers for the current letter
    pips_distribution = {
        'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None,
        'G': None, 'H': None, 'I': None, 'J': None, 'K': None, 'L': None,
        'M': None, 'N': None, 'O': None, 'P': None, 'Q': None, 'R': None,
        'S': None, 'T': None, 'U': None, 'V': None, 'W': None, 'X': None,
        'Y': None, 'Z': None
    }

    N = 2  # maximum integer value for each key
    keys = string.ascii_uppercase

    # generate all possible value combinations
    values = []
    for i in range(1, N + 1):
        values.append(list(range(1, i + 1)))

    # create dictionary combinations using itertools.product()
    combinations = []
    for combination in itertools.product(*values):
        dictionary = {}
        for i, value in enumerate(combination):
            dictionary[keys[i]] = value
        total_probability = calculate_probability(letter_frequencies, pips_distribution, dice_types[dice_type])

        combinations.append(dictionary)

    # print all combinations
    
    for combination in combinations:
        print(combination)

        total_probability = calculate_probability(letter_frequencies, pips_distribution, dice_types[dice_type])
        # Add the list of numbers to the table dictionary
        print(total_probability)
# Add the row for the D10 roll again case
table['E'] = [1, 1, 1, 0, 'Roll again']

# Print the final table
pp.pprint(table)
