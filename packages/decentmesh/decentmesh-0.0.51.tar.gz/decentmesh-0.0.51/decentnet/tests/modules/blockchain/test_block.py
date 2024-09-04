import unittest
from random import randint

from decentnet.consensus.blockchain_params import BlockchainParams
from decentnet.modules.blockchain.block import Block


class TestBlockSerialization(unittest.TestCase):
    def setUp(self):
        self.index = 1
        self.prev_hash = bytes.fromhex('abcd' * 8)  # 32 bytes of data
        self.difficulty = BlockchainParams.low_diff  # Assume a valid Difficulty object can be instantiated like this
        self.data = bytearray(b'some data for testing')

    def test_block_to_from_bytes(self):
        # Create a block
        block = Block(self.index, self.prev_hash, self.difficulty, self.data)

        # Serialize to bytes
        block_bytes = block.to_bytes()

        # Deserialize from bytes
        deserialized_block = Block.from_bytes(block_bytes)

        # Assert that the deserialized block matches the original block
        self.assertEqual(block.index, deserialized_block.index)
        self.assertEqual(block.previous_hash, deserialized_block.previous_hash)
        self.assertEqual(block.diff, deserialized_block.diff)
        self.assertEqual(block.data, deserialized_block.data)
        self.assertEqual(block.version, deserialized_block.version)
        self.assertEqual(block.nonce, deserialized_block.nonce)
        self.assertAlmostEqual(block.timestamp, deserialized_block.timestamp, places=5)

    def test_block_to_from_bytes_prevhash(self):
        # Create a block

        for _ in range(1000):
            non_empty_bytes_by4 = randint(1, 8)
            prev_hash = bytes.fromhex("00" * (16 - non_empty_bytes_by4)) + bytes.fromhex(
                'abcd' * non_empty_bytes_by4)
            block = Block(self.index, prev_hash, self.difficulty, self.data)

            # Serialize to bytes
            block_bytes = block.to_bytes()

            # Deserialize from bytes
            deserialized_block = Block.from_bytes(block_bytes)

            # Assert that the deserialized block matches the original block
            self.assertEqual(block.index, deserialized_block.index)
            self.assertEqual(block.previous_hash, deserialized_block.previous_hash)
            self.assertEqual(block.diff, deserialized_block.diff)
            self.assertEqual(block.data, deserialized_block.data)
            self.assertEqual(block.version, deserialized_block.version)
            self.assertEqual(block.nonce, deserialized_block.nonce)
            self.assertAlmostEqual(block.timestamp, deserialized_block.timestamp, places=5)


if __name__ == '__main__':
    unittest.main()
