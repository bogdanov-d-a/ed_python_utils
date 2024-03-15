def get_args_filename() -> str:
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    return args.filename


if __name__ == '__main__':
    from edpu.read_in_chunks import read_in_chunks
    from hashlib import sha1
    from sys import stdin, stdout

    hash_filename = get_args_filename()
    hasher = sha1()

    for chunk in read_in_chunks(stdin.buffer):
        hasher.update(chunk)
        stdout.buffer.write(chunk)

    with open(hash_filename, 'w') as hash_file:
        hash_file.write(hasher.hexdigest())
