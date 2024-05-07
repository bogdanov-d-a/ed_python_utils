def generate_ivs16_aes_cbc(count: int, key: bytes, iv: bytes) -> bytes:
    from .cryptography import generate_aes_cbc
    return generate_aes_cbc(count * 16, key, iv)


def get_ivs16_block(data: bytes, skip_blocks: int) -> bytes:
    from .utils import get_block
    return get_block(data, 16, skip_blocks)


def encrypt_block_aes_cbc(ot: bytes, key: bytes, ivs: bytes, block: int) -> bytes:
    from .cryptography import encrypt_aes_cbc
    ct = encrypt_aes_cbc(ot, key, get_ivs16_block(ivs, block))

    if len(ot) != len(ct):
        raise Exception('len(ot) != len(ct)')

    return ct


def decrypt_block_aes_cbc(ct: bytes, key: bytes, ivs: bytes, block: int) -> bytes:
    from .cryptography import decrypt_aes_cbc
    ot = decrypt_aes_cbc(ct, key, get_ivs16_block(ivs, block))

    if len(ot) != len(ct):
        raise Exception('len(ot) != len(ct)')

    return ot
