import math
from math import log


def get_bits_count(expected_elements, error_rate):
    """
    This function estimates the size of a bit-array and returns the count. It expects two inputs.
    expected_elements - is the number elements a bloom filter is expected to contain.
    error_rate - is the acceptable error rate of "False-Positive".
    The input ranges from 0 (0%) to 1 (100%).
    For an error rate of 1% the input value should be .01
    For an error rate of 10% the input value should be .1
    """
    x = -1 * (expected_elements * log(error_rate))
    y = log(2) ** 2  # base of the log functions is math.e
    array_size = x / y
    return int(round(array_size, 0))


def get_hash_func_count(bits_count, expected_elements):
    """
    This function returns the number of hash function we should use to manage each element
    and maintain the suggested error rate. This function accepts two inputs.
    bits_count - is the suggested size of the bit-array.
    (You can use the function get_bits_count to get this number.)
    expected_elements - is the number elements a bloom filter is expected to contain.
    """
    hash_count = (bits_count / expected_elements) * log(2)
    return int(round(hash_count, 0))


def get_false_positive_probability(hash_functions_count, total_entries, bloom_filter_size):
    """
    This function returns percentage of the probability of getting a false positive.
    It assumes that bits generated for input data overlap (collide).
    This function accepts 3 arguments.
    hash_functions_used - count of hash functions used.
    total_entries - entries added in the bloom filter so far.
    bloom_filter_size - the bit-array size.
    """
    x = 1 - 1/bloom_filter_size
    y = x ** (hash_functions_count * total_entries)
    z = (1 - y) ** hash_functions_count
    return round(z, 3)


if __name__ == "__main__":
    # Test - 1
    # expected_elements = 100
    # error_rate = .01
    # bits_array_size = get_bits_count(expected_elements, error_rate)
    # hash_func_count = get_hash_func_count(bits_array_size, expected_elements)
    # print(f"Expected elements - {expected_elements}\n"
    #       f"Error rate - {error_rate: .3%}\n"
    #       f"Array size - {bits_array_size}\n"
    #       f"Hash functions - {hash_func_count}")

    # Test measures false positive rate as data increases in a bloom filter
    # for count in range(10, 501, 10):
    #     fpr = get_false_positive_probability(hash_func_count, count, bits_array_size)
    #     print(f"For {count} elements the FPR-1 is {fpr:.3%}")
    hash_functions_used = 5
    entries_count = 43
    bloom_filter_array_size = 400
    fpr = get_false_positive_probability(hash_functions_used, entries_count, bloom_filter_array_size)
    print(f"Hash functions count = {hash_functions_used}, Entries = {entries_count}, and "
          f"Array size = {bloom_filter_array_size}: FPR is {fpr:.3%}")
