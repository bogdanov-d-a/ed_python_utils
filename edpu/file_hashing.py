import hashlib


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def hash_file(file_name, hasher):
    with open(file_name, 'rb') as file:
        for chunk in read_in_chunks(file):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha1_file(file_name):
    return hash_file(file_name, hashlib.sha1())


def sha512_file(file_name):
    return hash_file(file_name, hashlib.sha512())
