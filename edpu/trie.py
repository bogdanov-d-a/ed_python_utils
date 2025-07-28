# https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python


from typing import Any


_end = '_end_'


def make_trie(words: list[str]) -> dict[str, Any]:
    root: dict[str, Any] = {}

    for word in words:
        current_dict = root

        for letter in word:
            current_dict = current_dict.setdefault(letter, {})

        current_dict[_end] = _end

    return root


def in_trie(trie: dict[str, Any], word: str, prefix_mode: bool=False) -> bool:
    current_dict = trie

    for letter in word:
        if prefix_mode:
            if _end in current_dict:
                return True

        if letter not in current_dict:
            return False

        current_dict = current_dict[letter]

    return _end in current_dict
