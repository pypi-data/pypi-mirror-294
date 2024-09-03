import logging
from typing import Optional

import cbor2
from _cbor2 import CBORDecodeValueError
from ecdsa import VerifyingKey

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.cryptography.asymetric import AsymCrypt
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class Serializer:
    @staticmethod
    def serialize_data(
            public_key: VerifyingKey | str,
            signature: bytes,
            encrypted_data: bytes,
            target_pub_key: Optional[str] = None,
            cmd: Optional[int] = None,
            command_signature: Optional[bytes] = None,
            command_public_key: Optional[VerifyingKey] = None
    ) -> bytes:
        """Serializes public key, signature, and encrypted data and returns them as separate bytes.

        :returns: utf-8 encoded JSON
        """
        # Convert public_key to string if it's not already
        public_key_str = (
            public_key if isinstance(public_key, str)
            else AsymCrypt.verifying_key_to_string(public_key)
        )

        out = {
            "pub": public_key_str,
            "sig": signature,
            "data": encrypted_data,
            "target": target_pub_key
        }

        # Include command-related data only if cmd and command_signature are provided
        if cmd and command_signature:
            out.update({
                "cmd": cmd,
                "csig": command_signature,
                "cpub": AsymCrypt.verifying_key_to_string(command_public_key)
            })

        return cbor2.dumps(out)

    @staticmethod
    def deserialize_data(serialized_data: bytes) -> dict:
        """Deserializes the provided data and returns the public key, signature, and encrypted data."""
        try:
            deserialized_data = cbor2.loads(serialized_data)
        except (
                cbor2.CBORDecodeError, cbor2.CBORDecodeValueError,
                CBORDecodeValueError) as e:
            logger.error(f"Failed to decode cbor {serialized_data}")
            raise e
        try:
            if "sig" not in deserialized_data.keys():
                raise Exception(f"Corrupted data {deserialized_data}")
        except AttributeError as ex:
            raise Exception(f"Invalid data deserialized {ex}, data {deserialized_data}")

        return deserialized_data
