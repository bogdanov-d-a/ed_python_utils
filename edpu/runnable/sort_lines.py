if __name__ == '__main__':
    from sys import stdin

    print('\n'.join(sorted(
        stdin.read().split('\n')
    )))

    input()
