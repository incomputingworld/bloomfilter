from scalable_bloom_filter import (ScalableBloomFilter, marvel_characters,
                                   DC_characters)
from measurements import get_false_positive_probability

if __name__ == "__main__":
    # ====== ScalableBloomFilter ====
    # Create a new bloom filter once the limit is over.
    sbf = ScalableBloomFilter(10, .01,
                              2, .6)
    print(sbf)
    sbf.current_filter.total_entries = 10
    sbf.current_filter.bloom_filter_array[1:59] = 1
    if sbf.ready_to_create_new_filter():
        sbf.create_new_filter()
    print(sbf)

    # Add new entries and create new filter when existing filter fills up
    sbf1 = ScalableBloomFilter(10, .01,
                               2, .5)
    for character in marvel_characters:
        sbf1.add_new_data(character)
    print(sbf1)

    # This loop tests the existence of data in bloom filter.
    counter = 0
    for character in DC_characters:
        found = sbf1.data_exist(character)
        if found:
            counter += 1
            print(f"{character} exists in the bool filter.")
    print(f"Out of {len(DC_characters)} DC characters - {counter} are are in the list")

    # check the false positive rate of each of the bloom filter.
    for filter in sbf1.filters:
        print(get_false_positive_probability(filter.hash_func_count, filter.entries_added,
                                             filter.bloom_filter_size))
