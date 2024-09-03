import unittest

from decentnet.modules.blockchain.block import Block
from decentnet.modules.pow.difficulty import Difficulty
from decentnet.modules.serializer.serializer import Serializer
from decentnet.modules.transfer.packager import Packager


class TestPackager(unittest.TestCase):

    def setUp(self):
        self.owner_key_id = 1
        self.target_pub_key = "target_public_key"
        self.block = Block(0, b"0x0001", Difficulty(1, 8, 1, 1, 16), b"asdas")

    def test_pack(self):
        # Assuming necessary setup for KeyManager and AsymCrypt is done elsewhere

        packed_data = Packager.pack(self.owner_key_id, self.block, self.target_pub_key)
        self.assertIsInstance(packed_data, bytes)

    def test_unpack(self):
        packed_data = Packager.pack(self.owner_key_id, self.block, self.target_pub_key)

        verified, data, _ = Packager.unpack(packed_data)
        self.assertIsInstance(verified, bool)
        self.assertIsInstance(data, dict)
        self.assertIn("pub", data)
        self.assertIn("sig", data)
        self.assertIn("data", data)
        self.assertIn("target", data)

    def test_pack_unpack_cycle(self):
        # Pack the data
        packed_data = Packager.pack(self.owner_key_id, self.block, self.target_pub_key)
        self.assertIsInstance(packed_data, bytes)

        # Unpack the data
        verified, unpacked_data, _ = Packager.unpack(packed_data)
        self.assertTrue(verified, "The unpacked data should be verified")

        # Check if the data matches
        self.assertEqual(unpacked_data['data'], self.block.to_bytes(),
                         "Unpacked data should match the original block data")
        self.assertEqual(unpacked_data['target'], self.target_pub_key,
                         "Target public key should match")

    def test_pack_unpack_cycle_with_command(self):
        # Pack the data
        cmd = 1  # Example command
        packed_data = Packager.pack(self.owner_key_id, self.block, self.target_pub_key)

        verified, data, _ = Packager.unpack(packed_data)
        _data = Packager.add_cmd(data, owner_key_id=self.owner_key_id, cmd=cmd)
        serialized_broadcast = Serializer.serialize_data(_data["pub"],
                                                         _data["sig"],
                                                         _data["data"],
                                                         _data["target"],
                                                         _data["cmd"],
                                                         _data["csig"],
                                                         _data["cpub"])
        # Unpack and verify
        verified, unpacked_data, verified_csig = Packager.unpack(serialized_broadcast)

        self.assertTrue(verified, "The block signature verification failed.")
        self.assertIsNotNone(verified_csig,
                             "The command signature (csig) verification failed.")
        self.assertTrue(verified_csig, "The command signature (csig) is not valid.")


if __name__ == '__main__':
    unittest.main()
