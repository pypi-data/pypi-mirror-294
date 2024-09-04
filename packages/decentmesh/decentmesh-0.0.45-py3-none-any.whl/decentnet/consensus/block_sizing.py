"""Block Byte allocation for serialization and deserialization"""
from decentnet.__version__ import network_version

# This blocks maximum size is intentionally smaller
# to prevent DDOS attacks and ensure decentralized sending
MAXIMUM_BLOCK_SIZE = 4194304  # Bytes
BLOCK_PREFIX_LENGTH_BYTES = 3  # Bytes
INDEX_SIZE = 8  # Bytes
VERSION_SIZE = len(network_version)
NONCE_SIZE = 16  # Bytes
TIMESTAMP_SIZE = 8  # Bytes

MERGED_DIFFICULTY_BYTE_LEN = 13  # Bytes
HASH_LEN = 32  # Bytes
HASH_LEN_BLOCK = 48  # Bytes

RESERVE_BYTE_LEN = 77  # Bytes

MAXIMUM_DATA_SIZE = (MAXIMUM_BLOCK_SIZE - BLOCK_PREFIX_LENGTH_BYTES - INDEX_SIZE -
                     VERSION_SIZE - NONCE_SIZE - TIMESTAMP_SIZE -
                     MERGED_DIFFICULTY_BYTE_LEN - HASH_LEN -
                     HASH_LEN_BLOCK - RESERVE_BYTE_LEN)
