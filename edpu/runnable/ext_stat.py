if __name__ == '__main__':
    from edpu import pause_at_end

    def main() -> None:
        root = input()

        from edpu.ext_stat import ext_stat
        ext_stat(root)

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
