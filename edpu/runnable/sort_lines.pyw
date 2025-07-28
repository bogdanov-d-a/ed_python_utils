if __name__ == '__main__':
    from edpu.window_processor import run_with_exception_wrappers

    run_with_exception_wrappers([
        ('sort_lines', lambda s: '\n'.join(sorted(s.split('\n')))),
    ], 'sort_lines')
