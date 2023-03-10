import random

random.seed(10)

# Frequency of letters in English language
letter_similarities = {
    'A': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # a
    'B': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},  # b
    'C': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # c
    'D': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},  # d
    'E': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # e
    'F': {1, 4, 5, 6, 7, 8, 9, 10},  # f
    'G': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # g
    'H': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},  # h
    'I': {1, 4, 5, 6, 7, 8, 9, 10},  # i
    'J': {1, 4, 5, 6, 7, 8, 9, 10},  # j
    'K': {1, 3, 4, 5, 6, 7, 8, 9, 10},  # k
    'L': {1, 4, 5, 6, 7, 8, 9, 10},  # l
    'M': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # m
    'N': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # n
    'O': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # o
    'P': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},  # p
    'Q': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},  # q
    'R': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # r
    'S': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # s
    'T': {1, 3, 4, 5, 6, 7, 8, 9, 10},  # t
    'U': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # u
    'V': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # v
    'W': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # w
    'X': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},  # x
    'Y': {2, 3, 4, 5, 6, 7, 8, 9, 10},  # y
    'Z': {2, 3, 4, 5, 6, 7, 8, 9, 10}   # z
}

letter_frequencies = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.0236,
    'X': 0.0015,
    'Y': 0.01974,
    'Z': 0.00074
}

# letter_frequencies = {
#     'A': 0.26, 'B': 0.14, 'C': 0.2, 'D': 0.11, 'E': 0.09, 'F': 0.15, 'G': 0.05
# }

# sort the values of the frequencies
freq_sorted = sorted(letter_frequencies.values())
# calculate the smallest possible increment of the probability
min_diff = min([abs(item2 - item1) for item1, item2 in zip(freq_sorted[:-1], freq_sorted[1:])])

# estimate the minimal count of the pips required
freq_sums = [sum(freq_sorted[-i-1:]) for i, freq in enumerate(freq_sorted)]

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
    Additionally, recursive branches which are doomed to be off in distribution are killed in time
    to reduce computation effort.

    Args:
        n (int): The maximum value for each combination.
        m (int): The length of each combination.
        current (list): The current combination being generated.
        strings (list): The list of all possible combinations.
    """
    # If the length of the current combination is m, append it to the list of strings
    if m == 0:
        strings.append(''.join(map(str, current)))
        evaluate_combination(strings[-1])
        return

    # if len(current) >= (len(letter_frequencies) - min_pips_count - 1):
    # \
    #    or (len(_letter_distribution) == dice_types[dice_type]
    #        and all([len(letters) >= min_pips_count for letters in _letter_distribution.values()])):
    # Create a dictionary of letter-value pairs for the current combination
    _pips_distribution = {key: value for key, value in zip(letter_frequencies.keys(), current)}

    # Create a dictionary of pips-{set letters} pairs for the current combination
    # _letter_distribution = {value: {key for key, val in _pips_distribution.items() if val == value}
    #                        for value in _pips_distribution.values()}
    # Calculate the probability distribution of each letter appearing on the dice
    _total_probability = calculate_probability(_pips_distribution)

    # Check if the total probability of any letter is greater than the expected value for a fair dice
    if any([p > 1 / dice_types[dice_type] + min_diff
            if letter_frequencies[list(letter_frequencies)[i]] <= 1 / dice_types[dice_type]
            else False
            for i, p in enumerate(_total_probability)]):
        return

    if len(strings) >= 20:
        return

    # Generate all possible combinations by recursively adding values to the current combination
    for i in range(1, n+1):
        _generate_strings(n, m-1, current + [i], strings)


def calculate_probability(d: dict) -> list:
    """
    Calculate the probability of each value on the dice, given the frequency of each letter in the alphabet
    and the distribution of letters on the dice.

    Args:
        d (dict): A dictionary of letter-value pairs representing the distribution of letters on the dice.

    Returns:
        list: A list of the probability of each value on the dice.
    """
    # Initialize a list of probabilities for each value on the dice
    letter_distribution = {value: {key for key, val in d.items() if val == value} for value in d.values()}

    letter_freq_sum = {
        val: sum(letter_frequencies[char] for char in key)
        for val, key in letter_distribution.items()
    }

    p = letter_freq_sum.values()
    return p


def evaluate_combination(c):
    global weight_best
    # Create a dictionary of letter-value pairs for the current combination
    pips_distribution = {key: value for key, value in zip(letter_frequencies.keys(), c)}
    # Calculate the probability distribution of each letter appearing on the dice
    total_probability = calculate_probability(pips_distribution)
    # Calculate the weight of the current combination
    weight = sum([(p - 1 / dice_types[dice_type]) ** 2
                  if letter_frequencies[list(letter_frequencies)[i]] <= 1 / dice_types[dice_type]
                  else 0
                  for i, p in enumerate(total_probability)])
    # If the weight of the current combination is better than the best weight so far, update the pips distribution
    if weight <= weight_best:
        weight_best = weight
        pips_distribution_best[dice_type] = {key: (None
                                                   if letter_frequencies[key] >= 1 / dice_types[dice_type]
                                                   else value)
                                             for key, value in pips_distribution.items()}
        # Use a list comprehension to get a list of the values from the dictionary
        values_list = [value for value in pips_distribution.values()]

        # Use another list comprehension to count the occurrences of each value in the list
        value_counts = {value: values_list.count(value) for value in set(values_list)}

        print(weight, ':', [round(val, 5) for val in total_probability], ':', value_counts, ':', pips_distribution)


# A dictionary to store the best pips distribution for each dice type
# The keys are the dice types and the values are dictionaries of letter-value pairs
pips_distribution_best = {key: {} for key in dice_keys}

# Iterate over each dice type
for dice_type in dice_types.keys():
    print('solving column for', dice_type)

    # A variable to store the best weight so far
    weight_best = 1

    min_pips_count = [freq_sum + min_diff <= 1/dice_types[dice_type] for freq_sum in freq_sums].count(True)+1

    # Generate all possible combinations of values, break if required internally
    combinations = generate_strings(dice_types[dice_type], len(letter_frequencies.keys()))

    # # Iterate over each valid combination
    # for combination in combinations:
    #     evaluate_combination(combination)

# Print the best pips distribution for each dice type
print(pips_distribution_best)
