def idna_decode(line: str) -> str:
    return line.encode('ascii').decode('idna')


if __name__ == '__main__':
    from sys import stdin

    print('\n'.join(map(
        idna_decode,
        stdin.read().split('\n')
    )))

    input()
