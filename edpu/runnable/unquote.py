if __name__ == '__main__':
    from sys import stdin
    from urllib.parse import unquote

    print(unquote(stdin.read()))
    input()
