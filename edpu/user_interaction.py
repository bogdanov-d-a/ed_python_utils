from typing import Any


def list_to_dict(list_: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for key, value in list_:
        if key in result:
            raise Exception('key in result')
        result[key] = value

    return result


def yes_no_prompt(msg: str) -> bool:
    while True:
        print(msg + " (y/n)?")
        user_input = input().lower()

        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False


def pick_option(prompt: str, options: list[str]) -> int:
    index: int = 1
    for option in options:
        print(str(index) + '. ' + option)
        index += 1

    print(prompt)
    result = int(input())

    if result < 1:
        raise Exception('Number is too low')
    if result > len(options):
        raise Exception('Number is too high')

    return result - 1


def pick_option_multi(prompt: str, options: list[str]) -> set[int]:
    index: int = 1
    for option in options:
        print(str(index) + '. ' + option)
        index += 1

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


def pick_str_option(prompt: str, options: dict[str, str]) -> str:
    while True:
        for option_cmd, option_text in sorted(options.items()):
            print(option_cmd + ': ' + option_text)

        print(prompt)
        result = input()

        if result not in options:
            continue

        return result


def pick_str_option_ex(prompt: str, options: list[tuple[str, str, Any]]) -> Any:
    pick: dict[str, str] = list_to_dict(list(map(lambda e: (e[0], e[1]), options)))
    result = list_to_dict(list(map(lambda e: (e[0], e[2]), options)))
    return result[pick_str_option(prompt, pick)]
