# This implements a bloom filter as per the given estimated entries and desired error rate.

from bitarray import bitarray
from measurements import get_bits_count, get_hash_func_count
from hashes import hash_functions, crc32, hash128


class BloomFilter:
    def __init__(self, expected_entries, error_rate):
        self.expected_entries = expected_entries  # total number of elements expected
        self.error_rate = error_rate
        self.entries_added = 0  # number of entries added so far
        self.bloom_filter_size = 0  # number of bits needed for this BF
        self.hash_func_count = 0  # hash functions used by this BF

        self.bloom_filter_size = get_bits_count(self.expected_entries, self.error_rate)
        self.bloom_filter_array = bitarray(self.bloom_filter_size)  # bit-array

        self.hash_func_count = get_hash_func_count(self.bloom_filter_size, self.expected_entries)

    def add_new_data(self, data):
        """
        Adds new element (data) to a bloom filter
        Calculate indices for given data element. Uses get_bit_array_indices
        Pass these indices to function update_filter_array to update value to 1
        """
        indices = self.get_bit_array_indices(data)
        self.update_filter_array(indices)
        self.entries_added += 1

    def get_bit_array_indices(self, data):
        """
        Returns a list of indices for this data.
        Each index is an output of a hash function digest 'modulo-ed' by the bit array size.
        """

        # Identify the number of required hash functions. This limits to 12.
        max_hashes = len(hash_functions)
        if max_hashes >= self.hash_func_count:
            max_hashes = self.hash_func_count

        indices = []
        for hash_index in range(max_hashes):
            hash_func = hash_functions[hash_index]
            if hash_func == crc32:
                digest_value = hash_func(data.encode("utf-8"))
            elif hash_func == hash128:
                digest_value = hash_func(data.encode("utf-8"), signed=False)
            else:
                digest_value = self.get_hash_digest(hash_func, data)

            index = digest_value % self.bloom_filter_size
            indices.append(index)
        return indices

    def get_hash_digest(self, hash_func, data):
        """
        Generates a digest of the data from a given hash function.
        Returns the digest in integer format.
        """
        hash_obj = hash_func(data.encode("utf-8"))
        digest = hash_obj.hexdigest()
        digest = int(digest, 16)
        return digest

    def update_filter_array(self, indices):
        """
        Updates bloom filter array index with 1 for a given set of indices
        """
        for index in indices:
            self.bloom_filter_array[index] = 1

    def data_exist(self, data):
        """
        Checks if "data" exists in bloom filter or not. This function generates indices
        from the hash values using the hash functions.
        Compare all indices of the bloom filter against the generated indices.
        If the value at all the indices is 1, the function returns True.
        Otherwise, it returns False.
        """
        indices = self.get_bit_array_indices(data)
        print(f"{data} - {indices}")
        for index in indices:
            if self.bloom_filter_array[index] == 0:
                return False
        return True

    def __str__(self):
        output = ""
        output += (f'Expected Entries - {self.expected_entries}, \n'
                   f'Actual Entries - {self.entries_added},\n'
                   f'Bits Array size - {self.bloom_filter_size}, \n'
                   f'Error rate - {self.error_rate: .3%}, \n'
                   f'hash function count - {self.hash_func_count} \n')
        return output
