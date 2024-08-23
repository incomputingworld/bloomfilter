"""
Simple implementation of a bloom filter.

Third par libraries used:
1. bitarray library provides an object type which efficiently represents an array
of booleans. Bitarrays are sequence types and behave very much like usual lists.

2. murmurhash3 is a Python library for MurmurHash (MurmurHash3), a set of
fast and robust hash functions. We will use the function hash128 in this example
"""
from bitarray import bitarray
from mmh3 import hash128

bloom_filter_array = None
bloom_filter_array_size = 0


def add_new_data_to_bloom_filter(data):
    """
    Adds new data to a bloom filter
    """
    index = get_bit_array_index(data)
    # Print the data value and its calculated index
    print(f"{data} - {index}")
    update_bloom_filter_array(index)


def get_bit_array_index(data):
    """
    Returns an index to map the bit array for this data.
    """
    # generate hash value of the data
    digest_value = hash128(data.encode("utf-8"), signed=False)
    str.encode()
    # apply modulo operator to generate the index
    index = digest_value % bloom_filter_array_size
    return index


def update_bloom_filter_array(index):
    """
    Updates bloom filter array index with 1 for a given index
    """
    bloom_filter_array[index] = 1


def data_exist(data):
    """
    Checks if "data" exists in bloom filter. This function generates a hash value
    of the data using the same hash function we used to add new data.
    Then it generates an index from the hash value using modulo operator.
    in the bloom filter. If the value at the index is 1, the function returns True.
    Otherwise, it returns False.
    """
    index = get_bit_array_index(data)
    print(f"{data} - {index}")
    return bloom_filter_array[index] == 1


if __name__ == "__main__":
    # Using a small size of bit array, so it fills faster.
    bit_array_size = 20

    # Using bitarray module to create a bit array.
    bloom_filter_array = bitarray(bit_array_size)

    # length of the bloom filter. This value is same as "bit_array_size"
    bloom_filter_array_size = len(bloom_filter_array)

    print(f"Blank bloom filter - {bloom_filter_array}")
    # Output of above: Blank bloom filter - bitarray('00000000000000000000')

    # Add data to the bloom filter.
    avengers = ["Captain America", "Iron Man", "Blck Widow", "The Hulk",
                "Black Panther", "Spider man", "Thor", "Ant-Man",
                "Captain Marvel", "Hawk Eye", "Loki", "Daredevil"]
    for avenger in avengers:
        add_new_data_to_bloom_filter(avenger)

    print(f"Bloom filter with mapped values - {bloom_filter_array}")
    # Output of above: Bloom filter with mapped values - bitarray('00000011101001010010')

    print(f"Example of False Positive - ", end="")
    print(f"{data_exist("Super man")}")  # Outputs: Super man - 6 True
