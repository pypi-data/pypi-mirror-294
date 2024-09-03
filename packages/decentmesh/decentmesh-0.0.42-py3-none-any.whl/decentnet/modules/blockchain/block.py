import logging
import logging
import struct
import time
from typing import Union

from Crypto.Util.Padding import pad, unpad
from prometheus_client import Gauge

from decentnet.__version__ import network_version
from decentnet.consensus.block_sizing import MERGED_DIFFICULTY_BYTE_LEN, HASH_LEN, \
    INDEX_SIZE, VERSION_SIZE, NONCE_SIZE, TIMESTAMP_SIZE, HASH_LEN_BLOCK
from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.consensus.dev_constants import RUN_IN_DEBUG, BLOCK_ERROR_DATA_LOG_LEN
from decentnet.consensus.local_config import registry
from decentnet.modules.compression.wrapper import CompressionWrapper
from decentnet.modules.hash_type.hash_type import MemoryHash
from decentnet.modules.logger.log import setup_logger
from decentnet.modules.pow.difficulty import Difficulty
from decentnet.modules.pow.pow import PoW
from decentnet.modules.timer.timer import Timer

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)

data_header_ratio = Gauge('data_header_ratio', 'Header/Data Ratio', registry=registry)


class Block:
    index: int
    previous_hash: bytes = None
    version: bytes
    diff: Difficulty
    data: bytearray
    timestamp: float
    nonce: int | None
    _hash: MemoryHash | None
    ttc: float
    signature: str | None = None

    def __init__(self, index: int, prev_hash: bytes,
                 difficulty: Difficulty,
                 data: Union[bytearray, bytes]):
        self.index = index
        self.previous_hash = prev_hash
        self.data = data
        self.diff = difficulty
        self.timestamp = time.time()
        self.version = network_version
        self.nonce = 0
        self.signature = None

    def __str__(self):
        dd = str(bytes(self.data))
        display_data = dd[:BLOCK_ERROR_DATA_LOG_LEN] + "..." if len(
            dd) > BLOCK_ERROR_DATA_LOG_LEN else dd
        result = f"Block #{self.index}\n" \
                 f"Previous Hash: {self.previous_hash.hex()[2:].zfill(HASH_LEN) if self.index != 0 else 'GENESIS BLOCK'}\n" \
                 f"Version: {int.from_bytes(self.version, ENDIAN_TYPE)}\n" \
                 f"Difficulty: {self.diff}\n" \
                 f"Data: {display_data}\n" \
                 f"Timestamp: {self.timestamp}\n" \
                 f"Nonce: {self.nonce}\n"

        if hasattr(self, "_hash"):
            result += f"Hash: {self.hash.hex()[2:].zfill(HASH_LEN)}\n"

        return result

    @property
    def hash(self):
        return self.get_hash()

    def get_hash(self) -> bytes:
        barr = bytearray(self._hash.value)
        return bytes(barr)

    def compute_hash(self) -> MemoryHash:
        index_bytes = self.index.to_bytes(INDEX_SIZE, byteorder=ENDIAN_TYPE, signed=False)
        version_bytes = self.version
        diff_bytes = self.diff.to_bytes()
        previous_hash_bytes = self.previous_hash
        timestamp_bytes = struct.pack('d', self.timestamp)

        compressed_data = CompressionWrapper.compress_lz4(
            self.data)
        packed_block = (
                index_bytes + version_bytes + diff_bytes + previous_hash_bytes + timestamp_bytes + compressed_data)  # Speed up compression

        self._hash = MemoryHash(self.diff, packed_block)
        return self._hash

    def to_bytes(self) -> bytes:
        index_bytes = self.index.to_bytes(INDEX_SIZE, byteorder=ENDIAN_TYPE, signed=False)
        logger.debug(f"Index bytes size: {len(index_bytes)} bytes")

        # Version bytes (assuming it's already in bytes form)
        version_bytes = self.version
        logger.debug(f"Version bytes size: {len(version_bytes)} bytes")

        # Difficulty bytes (assuming it's already in bytes form, otherwise adapt accordingly)
        diff_bytes = self.diff.to_bytes()  # Replace with actual conversion if necessary
        logger.debug(f"Difficulty bytes size: {len(diff_bytes)} bytes")

        # Pad the previous hash and convert it to bytes
        previous_hash_bytes = pad(bytes(self.previous_hash), HASH_LEN_BLOCK, style='pkcs7')
        logger.debug(f"Previous hash bytes size: {len(previous_hash_bytes)} bytes")

        nonce_bytes = self.nonce.to_bytes(NONCE_SIZE, byteorder=ENDIAN_TYPE,
                                          signed=False)
        timestamp_bytes = struct.pack('d', self.timestamp)

        compressed_data = CompressionWrapper.compress_lz4(
            self.data)

        packed_block = (index_bytes + version_bytes + diff_bytes + previous_hash_bytes +
                        nonce_bytes + timestamp_bytes + compressed_data)  # Speed up compression

        packed_block_len = len(packed_block)
        compressed_data_len = len(compressed_data)

        data_header_ratio.set(
            (packed_block_len - compressed_data_len) / compressed_data_len)

        logger.debug(f"Packed Block into {packed_block_len} B")
        return packed_block

    @classmethod
    def from_bytes(cls, compressed_block_bytes: bytes):
        block = cls.__new__(cls)

        block_bytes = memoryview(compressed_block_bytes)

        cursor = 0

        # Unpack index
        block.index = int.from_bytes(block_bytes[cursor:cursor + INDEX_SIZE], byteorder=ENDIAN_TYPE,
                                     signed=False)
        cursor += INDEX_SIZE

        # Unpack version directly
        block.version = block_bytes[cursor:cursor + VERSION_SIZE]
        cursor += VERSION_SIZE

        # Unpack difficulty
        block.diff = Difficulty.from_bytes(block_bytes[cursor:cursor + MERGED_DIFFICULTY_BYTE_LEN])
        cursor += MERGED_DIFFICULTY_BYTE_LEN

        # Unpack previous hash
        block.previous_hash = unpad(bytes(block_bytes[cursor:cursor + HASH_LEN_BLOCK]), HASH_LEN_BLOCK,
                                    style='pkcs7')
        cursor += HASH_LEN_BLOCK

        # Unpack nonce
        block.nonce = int.from_bytes(block_bytes[cursor:cursor + NONCE_SIZE],
                                     byteorder=ENDIAN_TYPE,
                                     signed=False)
        cursor += NONCE_SIZE

        # Unpack timestamp
        block.timestamp = struct.unpack("d", block_bytes[cursor:cursor + TIMESTAMP_SIZE])[0]
        cursor += TIMESTAMP_SIZE

        # Decompress the remaining data
        block.data = CompressionWrapper.decompress_lz4(block_bytes[cursor:])

        return block

    def mine(self, measure=False):
        logger.debug(f"Mining block #{self.index}")
        if measure:
            t = Timer()

        a = self.compute_hash()

        finished_hash, finished_nonce = PoW.compute(a, self.diff.n_bits)
        self.nonce = finished_nonce

        if measure:
            self.ttc = t.stop()
            return finished_nonce, self.ttc
        else:
            return finished_nonce
