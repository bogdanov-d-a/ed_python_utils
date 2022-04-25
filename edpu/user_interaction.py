def yes_no_prompt(msg):
    while True:
        print(msg + " (y/n)?")
        user_input = input().lower()

        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False


def pick_option(prompt, options):
    index = 1
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


def pick_option_multi(prompt, options):
    index = 1
    for option in options:
        print(str(index) + '. ' + option)
        index += 1

    print(prompt)
    selection = set()

    while True:
        print_data = []
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
