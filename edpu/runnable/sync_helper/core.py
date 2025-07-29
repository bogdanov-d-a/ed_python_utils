def main() -> None:
    while True:
        from subprocess import run
        run([
            'sync64',
            '-r',
        ], check=True)

        print()
        print()

        from edpu.user_interaction import accent_print
        accent_print(['WAITING FOR INPUT...'])

        input()


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
