from typing import Callable


def pick(get_stop: Callable[[], bool], get_bootstrap_mode: Callable[[], bool], filename: str, debug: bool) -> None:
    while not get_stop():
        from ... import user_interaction
        from ..utils import actions

        actions_dict = user_interaction.list_to_dict(list(map(lambda action: (action.cmd, action.name), actions.all())))
        action_cmd = user_interaction.pick_str_option('Pick action', actions_dict)
        action = actions.find_by_cmd(action_cmd)

        if action.in_place:
            action.handler()

        else:
            from ..utils.utils import Args
            cmd = Args(action_cmd, get_bootstrap_mode()).build_cmd(filename)

            if debug:
                print(f'run_action {cmd}')
                input()

            else:
                from edpu_user.python_launcher import start_with_python3
                start_with_python3(cmd, '.')
