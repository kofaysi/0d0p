# Frequency of letters in English language
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

# sort the values of the frequencies
freq_sorted = sorted(letter_frequencies.values())

# calculate the smallest possible increment of the probability
min_diff = min([abs(item2 - item1) for item1, item2 in zip(freq_sorted[:-1], freq_sorted[1:])])
# min_freq = min(freq_sorted)

# estimate the minimal count of the pips required
freq_sums = [sum(freq_sorted[-i-1:]) for i, freq in enumerate(freq_sorted)]

dice_keys = ['D10']  # 'D2', 'D4', 'D6', 'D8',

# A list of all uppercase letters in the English alphabet
dice_types = {key: int(key[1:]) for key in dice_keys}

# margin of acceptance to the p_mean
p_mean_margin = 0.1


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
    _generate_strings(n, m, [], strings, {})
    return strings


def _generate_strings(n: int, m: int, current: list, strings: list, current_probability: dict) -> None:
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
        strings.append(current)
        evaluate_combination(strings[-1])
        return

    # Create a dictionary of letter-value pairs for the current combination
    if current:
        _new_dice = current[-1]
        _new_position = len(current) - 1
        _new_letter = list(letter_frequencies.keys())[_new_position]
        _new_freq = letter_frequencies[_new_letter] if letter_frequencies[_new_letter] is not None else 0
        if _new_freq is None:
            pass

        current_probability[_new_dice] = current_probability.get(_new_dice, 0) + _new_freq

        # Check if the total probability of the new letter after new addition is greater than
        # the expected value for a fair dice
        if current_probability[_new_dice] > (1 + p_mean_margin) * p_mean:
            return

    # if len(strings) >= 10000:
    #    return

    # Generate all possible combinations by recursively adding values to the current combination
    for i in range(1, n+1):
        _generate_strings(n, m-1, current + [i], strings, dict(current_probability))


def calculate_probability(d: dict) -> dict:
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
        val: sum(letter_frequencies[char] if val is not None else 0 for char in key)
        for val, key in letter_distribution.items()
    }
    return letter_freq_sum


def evaluate_combination(c):
    global weight_best
    # Create a dictionary of letter-value pairs for the current combination
    pips_distribution = distribute_pips(c)

    # Calculate the probability distribution of each letter appearing on the dice
    pips_probability = calculate_probability(pips_distribution)

    # Calculate the weight of the current combination
    weight = sum([(p - p_mean) ** 2 for p in pips_probability.values()])

    # If the weight of the current combination is better than the best weight so far, update the pips distribution
    if weight <= weight_best:
        weight_best = weight
        pips_distribution_best[dice_type] = pips_distribution

        # Use a list comprehension to get a list of the values from the dictionary
        values_list = [value for value in pips_distribution.values()]

        # Use another list comprehension to count the occurrences of each value in the list
        value_counts = {value: values_list.count(value) for value in set(values_list)}

        print(weight, ':',
              {key: round(val, 5) for key, val in pips_probability.items()}, ':',
              value_counts, ':',
              pips_distribution)


def distribute_pips(c):
    pips_distribution = {key: value if letter_frequencies[key] is not None
                                       and letter_frequencies[key] < (1 + p_mean_margin) * p_mean else None
                         for key, value in zip(letter_frequencies.keys(), c)}
    return pips_distribution


# A dictionary to store the best pips distribution for each dice type
# The keys are the dice types and the values are dictionaries of letter-value pairs
pips_distribution_best = {key: {} for key in dice_keys}

# Iterate over each dice type
for dice_type in dice_types.keys():
    print('solving column for', dice_type)

    # A variable to store the best weight so far
    weight_best = 1

    # the average frequency or probability
    p_mean = 1/dice_types[dice_type]

    while any([f is not None and f > (1 + p_mean_margin) * p_mean for f in letter_frequencies.values()]):
        sum_letter_freq = sum([f if f is not None and f <= p_mean else 0 for f in letter_frequencies.values()])
        letter_frequencies.update((key, 1/sum_letter_freq*f if f is not None and f <= p_mean else None)
                                  for key, f in letter_frequencies.items())

    min_pips_count = [freq_sum <= (1 + p_mean_margin) * p_mean for freq_sum in freq_sums].count(True)+1

    # Generate all possible combinations of values, break if required internally
    combinations = generate_strings(dice_types[dice_type], len(letter_frequencies.keys()))
