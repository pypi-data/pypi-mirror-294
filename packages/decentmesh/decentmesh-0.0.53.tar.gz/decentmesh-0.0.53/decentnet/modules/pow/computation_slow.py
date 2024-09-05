from decentnet.modules.pow.pow_utils import PowUtils


def compute_pow(n_bits, hash_t, nonce):
    _bits = hash_t.diff.hash_len_chars * 8 - n_bits
    # Clone the original hash_t to avoid modifying the original object

    while PowUtils.get_bit_length(hash_t, nonce, hash_t.diff) > _bits:
        nonce += 1

    # Return the correct nonce but do not modify the original hash_t
    return nonce
