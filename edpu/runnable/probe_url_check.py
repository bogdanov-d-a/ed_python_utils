if __name__ == '__main__':
    from edpu import pause_at_end

    def main() -> None:
        from edpu.probe_url import probe_url

        print('probe_url')
        url = input()
        print('\n'.join(probe_url(url)))

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
