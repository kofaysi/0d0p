# Frequency of letters in English language
letter_frequencies = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
    'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
    'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.01974, 'Z': 0.00074
}

# letter_frequencies = {
#     'A': 0.26, 'B': 0.14, 'C': 0.2, 'D': 0.11, 'E': 0.09, 'F': 0.15, 'G': 0.05
# }

# sort the values of the frequencies
freq_sorted = sorted(letter_frequencies.values())
# calculate the smallest possible increment of the probability
diff = min([abs(item1-item2) for item1, item2 in zip(freq_sorted[:-1], freq_sorted[1:])])

dice_keys = ['D2', 'D4', 'D6', 'D8', 'D10']
# A list of all uppercase letters in the English alphabet
dice_types = {key: int(key[1:]) for key in dice_keys}


def generate_strings(n: int, m: int) -> list:
    """
    Generate all possible combinations of values of length m, where each value is between 1 and n.

    Args:
        n (int): The maximum value for each combination.
        m (int): The length of each combination.

    Returns:
        list: A list of strings representing all possible combinations.
    """
    strings = []
    _generate_strings(n, m, [], strings)
    return strings


def _generate_strings(n: int, m: int, current: list, strings: list) -> None:
    """
    Helper function for generate_strings. Recursively generates all possible combinations of values.

    Args:
        n (int): The maximum value for each combination.
        m (int): The length of each combination.
        current (list): The current combination being generated.
        strings (list): The list of all possible combinations.
    """
    # If the length of the current combination is m, append it to the list of strings
    if m == 0:
        strings.append(''.join(map(str, current)))
        return

    # Create a dictionary of letter-value pairs for the current combination
    _pips_distribution = {key: value for key, value in zip(letter_frequencies.keys(), current)}
    # Calculate the probability distribution of each letter appearing on the dice
    _total_probability = calculate_probability(letter_frequencies, _pips_distribution, dice_types[dice_type])

    # Check if the total probability of any letter is greater than the expected value for a fair dice
    if any([p > 1/dice_types[dice_type] + diff/2 for p in _total_probability]):
        return

    # Generate all possible combinations by recursively adding values to the current combination
    for i in range(1, n+1):
        _generate_strings(n, m-1, current + [i], strings)


def calculate_probability(f: dict, d: dict, n: int) -> list:
    """
    Calculate the probability of each value on the dice, given the frequency of each letter in the alphabet
    and the distribution of letters on the dice.

    Args:
        f (dict): A dictionary of letter-frequency pairs.
        d (dict): A dictionary of letter-value pairs representing the distribution of letters on the dice.
        n (int): The number of sides on the dice.

    Returns:
        list: A list of the probability of each value on the dice.
    """
    # Initialize a list of probabilities for each value on the dice
    p = [0] * n

    # Iterate over each letter and its frequency
    for letter, freq in f.items():
        # Iterate over each possible value on the dice
        for i in range(1, n + 1):
            # If the value for the current letter on the dice is equal to the current value, update its probability
            if int(d.get(letter, 0)) == i:
                p[i - 1] += freq
    return p


# A dictionary to store the best pips distribution for each dice type
# The keys are the dice types and the values are dictionaries of letter-value pairs
pips_distribution_best = {key: {} for key in dice_keys}

# A variable to store the best weight so far
weight_best = 1

# Iterate over each dice type
for dice_type in dice_types.keys():
    print('solving column for', dice_type)
    # Generate all possible combinations of values
    strings_valid = generate_strings(dice_types[dice_type], len(letter_frequencies.keys()))

    # Iterate over each valid combination
    for string in strings_valid:
        # Create a dictionary of letter-value pairs for the current combination
        pips_distribution = {key: value for key, value in zip(letter_frequencies.keys(), string)}

        # Calculate the probability distribution of each letter appearing on the dice
        total_probability = calculate_probability(letter_frequencies, pips_distribution, dice_types[dice_type])

        # Calculate the weight of the current combination
        weight = sum([(p - 1 / dice_types[dice_type]) ** 2 if letter_frequencies[list(letter_frequencies)[i]] <= 1 / dice_types[dice_type] else 0 for i, p in enumerate(total_probability)])

        # If the weight of the current combination is better than the best weight so far, update the pips distribution
        if weight < weight_best:
            weight_best = weight
            pips_distribution_best[dice_type] = {key: (None if letter_frequencies[key] >= 1 / dice_types[dice_type] else value) for key, value in pips_distribution.items()}
            print(weight, ':', pips_distribution)

# Print the best pips distribution for each dice type
print(pips_distribution_best)
