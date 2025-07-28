def main() -> None:
    while True:
        from edpu.user_interaction import yes_no_prompt
        from os import system

        system('sync64 -r')

        if not yes_no_prompt('Run again'):
            break


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
