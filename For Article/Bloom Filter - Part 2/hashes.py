import hashlib
from hashlib import (blake2b, blake2s, md5, sha1, sha224, sha256,
                     sha384, sha3_224, sha3_256, sha3_384)
from zlib import crc32
from mmh3 import hash128

hash_functions = [crc32, hash128, blake2b, blake2s, md5, sha1,
                  sha224, sha256, sha384, sha3_224, sha3_256, sha3_384]


