if __name__ == '__main__':
    from edpu.explorer_lifecycle import ExplorerDown

    with ExplorerDown():
        from edpu.user_interaction import user_wait
        user_wait('ExplorerDown')
