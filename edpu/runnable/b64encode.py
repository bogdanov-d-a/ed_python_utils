if __name__ == '__main__':
    from base64 import b64encode
    from sys import stdin

    print(b64encode(stdin.read().encode()).decode('ascii'))
    input()
