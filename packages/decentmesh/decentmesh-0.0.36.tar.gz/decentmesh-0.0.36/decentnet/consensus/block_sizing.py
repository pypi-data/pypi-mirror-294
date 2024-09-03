"""Block Byte allocation for serialization and deserialization"""
from decentnet.__version__ import network_version

BLOCK_PREFIX_LENGTH_BYTES = 2
MAXIMUM_BLOCK_SIZE = 65536  # Bytes
INDEX_SIZE = 8
VERSION_SIZE = len(network_version)
NONCE_SIZE = 16
TIMESTAMP_SIZE = 8

MERGED_DIFFICULTY_BYTE_LEN = 13
HASH_LEN = 32
HASH_LEN_BLOCK = 48
