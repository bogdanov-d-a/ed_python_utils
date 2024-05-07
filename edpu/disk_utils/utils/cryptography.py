from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.modes import CBC


def secure_random(bytes: int) -> bytes:
    from os import urandom
    return urandom(bytes)


def cipher_aes_cbc(key: bytes, iv: bytes) -> Cipher[CBC]:
    from cryptography.hazmat.primitives.ciphers.algorithms import AES
    return Cipher(AES(key), CBC(iv))


def encrypt_aes_cbc(ot: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = cipher_aes_cbc(key, iv)
    encryptor = cipher.encryptor()
    return encryptor.update(ot) + encryptor.finalize()


def decrypt_aes_cbc(ct: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = cipher_aes_cbc(key, iv)
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()


def generate_aes_cbc(bytes: int, key: bytes, iv: bytes) -> bytes:
    result = encrypt_aes_cbc(b'\x00' * bytes, key, iv)

    if len(result) != bytes:
        raise Exception('len(result) != bytes')

    return result
