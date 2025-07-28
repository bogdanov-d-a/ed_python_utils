if __name__ == '__main__':
    from edpu.user_interaction import pick_str_option_ex
    from edpu.win_service_control import run_sc, QUERY, STOP

    action = pick_str_option_ex('win_divert action', list(map(
        lambda item: (item[0], item[1], item[1]),
        [
            ('q', QUERY),
            ('s', STOP),
        ]
    )))

    run_sc(action, 'WinDivert')
