if __name__ == '__main__':
    from edpu.str_check import str_check
    from edpu.window_processor import run_with_exception_wrappers

    run_with_exception_wrappers([
        ('str_check', str_check),
    ], 'str_check')
