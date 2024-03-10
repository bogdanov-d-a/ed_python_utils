def run(action_cmd: str, bootstrap: bool) -> None:
    from ..utils.actions import find_by_cmd

    print('action == ' + action_cmd)
    print('bootstrap == ' + str(bootstrap))
    print()

    action = find_by_cmd(action_cmd)

    if action.in_place:
        raise Exception('unsupported in-place action ' + action_cmd)

    action.handler()
