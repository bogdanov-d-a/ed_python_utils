def escape_with_char(s: str, what: str, with_what: str) -> str:
    return s.replace(what, with_what + what)


def escape_with_char_double(s: str, char: str) -> str:
    return s.replace(char, char * 2)


def translate(s: str, trans: dict[str, str]) -> str:
    return s.translate(str.maketrans(trans))
