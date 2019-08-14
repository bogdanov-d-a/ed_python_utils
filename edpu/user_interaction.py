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
