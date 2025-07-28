if __name__ == '__main__':
    from edpu.window_processor import run_with_exception_wrappers

    run_with_exception_wrappers([
        ('lower', lambda s: s.lower()),
        ('upper', lambda s: s.upper()),
    ], 'case_converter')
