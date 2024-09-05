import pyximport
import rich

from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.modules.pow.hashing import hash_func

pyximport.install()
try:
    from decentnet.modules.pow.computation_fast import int_to_bytes  # noqa
except ImportError as ex:
    rich.print(f"[red]POW Operating in low hashrate mode, more instructions: {ex}[/red]")
    from decentnet.modules.convert.byte_operations import int_to_bytes


class PowUtils:
    @staticmethod
    def get_bit_length(i_hash, nonce, diff) -> int:
        return PowUtils.value_as_int(
            hash_func(int_to_bytes(i_hash.value_as_int() + nonce), diff)).bit_length()

    @staticmethod
    def value_as_int(value) -> int:
        return int.from_bytes(value, ENDIAN_TYPE)
