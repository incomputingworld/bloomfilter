from bloom_filter import BloomFilter
from input_data import marvel_characters, DC_characters
from measurements import get_false_positive_probability

if __name__ == "__main__":
    # Create a new bloom filter.
    # expected_entries = 100
    # error_rate = .01
    # bf = BloomFilter(expected_entries, error_rate)
    # print(bf)

    # Create a new bloom filter and add data
    expected_entries = 50
    error_rate = .01
    bf1 = BloomFilter(expected_entries, error_rate)
    for character in marvel_characters:
        bf1.add_new_data(character)
    print(bf1)

    # Check the false positive rate after filling the data.
    print(f"False-positive probability is - "
          f"{get_false_positive_probability(bf1.hash_func_count, 
                                            bf1.entries_added,
                                            bf1.bloom_filter_size): .3%}")

    # Look for data that does not exist in the filter.
    counter = 0
    for character in DC_characters:
        found = bf1.data_exist(character)
        if found:
            counter += 1
        print(found)
    print(f"Out of {len(DC_characters)} DC characters - {counter} are in the list")
