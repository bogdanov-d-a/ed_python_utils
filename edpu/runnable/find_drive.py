if __name__ == '__main__':
    from edpu import pause_at_end
    from edpu.find_drive import find_drive

    pause_at_end.run(lambda: find_drive({
        'C:\\': 'Windows',
    }))
