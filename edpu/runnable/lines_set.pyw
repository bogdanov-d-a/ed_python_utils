if __name__ == '__main__':
    from edpu.window_processor import run_with_exception_wrappers

    run_with_exception_wrappers([
        ('lines_set', lambda s: '\n'.join(sorted(set(s.split('\n'))))),
    ], 'lines_set')
