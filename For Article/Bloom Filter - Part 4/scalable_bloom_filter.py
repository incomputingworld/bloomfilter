#  Scalable bloom filter. Implementing using a class.

from bitarray import bitarray
from input_data import marvel_characters, DC_characters
from measurements import (get_bits_count, get_hash_func_count,
                          get_false_positive_probability)
from hashes import hash_functions, crc32, hash128


class ScalableBloomFilter:
    def __init__(self, expected_entries=10, error_rate=.01,
                 growth_factor=2, load_threshold=.7):
        self.filters = []
        self.growth_factor = growth_factor
        self.load_threshold = load_threshold
        self.current_filter = self._add_new_filter(expected_entries, error_rate,
                                                   self.load_threshold)
        self.filters.append(self.current_filter)

    def _add_new_filter(self, expected_entries, error_rate, load_threshold):
        return BloomFilter(expected_entries, error_rate, load_threshold)

    def load_threshold_full(self):
        return self.current_filter.load_threshold_full()

    def add_new_data(self, data):
        self.current_filter.add_new_data(data)
        if self.ready_to_create_new_filter():
            self.create_new_filter()

    def ready_to_create_new_filter(self):
        if self.current_filter.entries_added < self.current_filter.expected_entries:
            return False
        if not self.load_threshold_full():
            return False
        return True

    def create_new_filter(self):
        expected_entries = self.current_filter.expected_entries * self.growth_factor
        error_rate = self.current_filter.error_rate / self.growth_factor
        self.current_filter = self._add_new_filter(expected_entries, error_rate,
                                                   self.load_threshold)
        self.filters.append(self.current_filter)

    def data_exist(self, data):
        for filter in reversed(self.filters):
            if filter.data_exist(data):
                return True
        return False

    def __str__(self):
        output = f"Scalable Bloom filter with - {len(self.filters)} filters\n"
        for filter in self.filters:
            output += (f'Expected Entries - {filter.expected_entries}, \n'
                       f'Actual Entries - {filter.entries_added},\n'
                       f'Bits Array size - {filter.bloom_filter_size}, \n'
                       f'Load threshold - {filter.load_threshold}, \n'
                       f'Error rate - {filter.error_rate: .2%}, \n'
                       f'hash function count - {filter.hash_func_count} \n\n')
        return output


class BloomFilter:
    def __init__(self, expected_entries, error_rate, load_threshold):
        self.expected_entries = expected_entries
        self.error_rate = error_rate
        self.load_threshold = load_threshold
        self.entries_added = 0
        self.bloom_filter_size = get_bits_count(self.expected_entries, self.error_rate)
        self.hash_func_count = get_hash_func_count(self.bloom_filter_size,
                                                   self.expected_entries)
        self.bloom_filter_array = bitarray(self.bloom_filter_size)

    def add_new_data(self, data):  # adds new data to a bloom filter
        indexes = self.get_bit_array_indices(data)
        self.update_filter_array(indexes)
        self.entries_added += 1

    def get_bit_array_indices(self, data):
        max_hashes = len(hash_functions)
        if max_hashes >= self.hash_func_count:
            max_hashes = self.hash_func_count
        indexes = []
        for hash_index in range(max_hashes):
            hash_func = hash_functions[hash_index]
            digest_value = self.get_hash_digest(hash_func, data)
            index_value = digest_value % self.bloom_filter_size
            indexes.append(index_value)
        return indexes

    def get_hash_digest(self, hash_func, data):
        digest_value = 0
        if hash_func == crc32:
            digest_value = hash_func(data.encode("utf-8"))
        elif hash_func == hash128:
            digest_value = hash_func(data.encode("utf-8"), signed=False)
        else:
            hash_obj = hash_func(data.encode("utf-8"))
            digest_value = hash_obj.hexdigest()
            digest_value = int(digest_value, 16)
        return digest_value

    def update_filter_array(self, indexes):
        for index in indexes:
            self.bloom_filter_array[index] = 1

    def load_threshold_full(self):
        active_bits_count = self.bloom_filter_array.count(1)
        return active_bits_count >= self.bloom_filter_size * self.load_threshold

    def data_exist(self, data):
        indexes = self.get_bit_array_indices(data)
        print(f"{data} - {indexes}")
        for index in indexes:
            if self.bloom_filter_array[index] == 0:
                return False
        return True
