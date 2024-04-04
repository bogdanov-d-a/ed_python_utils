if __name__ == '__main__':
    from base64 import b64decode
    from sys import stdin

    print(b64decode(stdin.read()).decode())
    input()
