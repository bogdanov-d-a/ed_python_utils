if __name__ == '__main__':
    from typing import Optional

    def encode_(char: str, encoding: str='utf-8') -> bytes:
        return char.encode(encoding)

    def encode_list(char_list: list[str], encoding: str='utf-8') -> list[bytes]:
        return list(map(
            lambda char: encode_(char, encoding),
            char_list
        ))

    def try_encode_list(char_list: list[str], encoding: str='utf-8') -> Optional[str]:
        try:
            encode_list(char_list, encoding)
            return None
        except Exception as e:
            return str(e)

    def main() -> None:
        from sys import stdin

        str_ = stdin.read()
        print()

        print(f'len(\'{str_}\') = {len(str_)}')
        print()

        str_list = list(str_)

        print(f'break = {str_list}')
        print()

        print(f'break_b = {encode_list(str_list)}')
        print()

        str_set = sorted(set(str_list))

        print(f'set = {str_set}')
        print()

        print(f'set_b = {encode_list(str_set)}')
        print()

        print('is ascii' if str_.isascii() else 'is *NOT* ascii')
        print()

        def encoding_test() -> None:
            from edpu.all_encodings import all_encodings

            for encoding in all_encodings():
                error = try_encode_list(str_set, encoding)
                print(f'{encoding} = {'OK' if error is None else error}')

        input()
        encoding_test()

        input()

    main()
