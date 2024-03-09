from .context_manager import DummyContextManager
from typing import Any, Callable, Optional, TypeVar


T = TypeVar('T')


def list_to_dict(list_: list[tuple[str, T]]) -> dict[str, T]:
    result: dict[str, T] = {}

    for key, value in list_:
        if key in result:
            raise Exception('key in result')
        result[key] = value

    return result


def generate_cmds(list_: list[T]) -> list[tuple[str, T]]:
    cmds = '1234567890qwertyuiopasdfghjklzxcvbnm'

    if len(list_) > len(cmds):
        raise Exception('list is too long')

    return list(zip(cmds[:len(list_)], list_))


def yes_no_prompt(msg: str) -> bool:
    while True:
        print(msg + " (y/n)?")
        user_input = input().lower()

        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False


def pick_option(prompt: str, options: list[str]) -> int:
    for option, index in zip(options, range(len(options))):
        print(str(index + 1) + '. ' + option)

    print(prompt)
    result = int(input())

    if result < 1:
        raise Exception('Number is too low')
    if result > len(options):
        raise Exception('Number is too high')

    return result - 1


def pick_option_multi(prompt: str, options: list[str]) -> set[int]:
    for option, index in zip(options, range(len(options))):
        print(str(index + 1) + '. ' + option)

    print(prompt)
    selection: set[int] = set()

    while True:
        print_data: list[str] = []
        for selection_item in selection:
            print_data.append(options[selection_item])
        print(', '.join(print_data))

        user_data_str = input()
        try:
            user_data = int(user_data_str)
        except:
            print('Not a number')
            continue

        if user_data == 0:
            return selection

        if user_data < 1:
            print('Number is too low')
        elif user_data > len(options):
            print('Number is too high')
        else:
            if user_data - 1 in selection:
                selection.remove(user_data - 1)
            else:
                selection.add(user_data - 1)


def pick_str_option(prompt: str, options: dict[str, str], print_lock: Any=DummyContextManager()) -> str:
    while True:
        with print_lock:
            for option_cmd, option_text in sorted(options.items()):
                print(option_cmd + ': ' + option_text)

            print(prompt)

        result = input()

        if result not in options:
            continue

        return result


def pick_str_option_ex(prompt: str, options: list[tuple[str, str, T]], print_lock: Any=DummyContextManager()) -> T:
    pick = list_to_dict(list(map(lambda e: (e[0], e[1]), options)))
    result = list_to_dict(list(map(lambda e: (e[0], e[2]), options)))
    return result[pick_str_option(prompt, pick, print_lock)]


def pick_str_option_multi(prompt: str, options: list[tuple[str, str]], validator: Callable[[set[str]], Optional[str]]=lambda _: None) -> list[str]:
    option_cmds = set(map(lambda e: e[0], options))

    for option_cmd in option_cmds:
        if len(option_cmd) != 1:
            raise Exception('incorrect option command ' + option_cmd + ' found')

    def get_user_char_set() -> Optional[set[str]]:
        user_str = input()

        user_char_set: set[str] = set()

        for user_char in user_str:
            if user_char not in option_cmds:
                print('unexpected char ' + user_char + ' found')
                return None

            if user_char in user_char_set:
                print('duplicate char ' + user_char + ' found')
                return None

            user_char_set.add(user_char)

        validator_result = validator(user_char_set)
        if validator_result is not None:
            print(validator_result)
            return None

        return user_char_set

    while True:
        for option_cmd, option_text in options:
            print(option_cmd + ': ' + option_text)

        print(prompt)

        result = get_user_char_set()

        if result is None:
            continue

        return list(result)
