from typing import Any

def run(user_data: dict[str, Any]) -> None:
    from .. import pause_at_end

    def main() -> None:
        from ..user_interaction import pick_str_option_ex
        from .facades.bundle.apply import apply_bundle
        from .facades.bundle.create import create_bundle
        from .facades.compare_definitions import compare_definitions
        from .facades.find_recycle_dirs import find_recycle_dirs
        from .facades.update.data import update_data
        from .facades.update.definition import update_definition
        from .utils.mp_global import init
        from .utils.user_data import UserData
        from typing import Callable

        init()

        actions: list[tuple[str, str, Callable[[UserData], None]]] = [
            ('ba', 'Apply bundle', apply_bundle),
            ('bc', 'Create bundle', create_bundle),
            ('c', 'Compare definitions (diff tool)', compare_definitions),
            ('r', 'Find recycle dirs', find_recycle_dirs),
            ('s', 'Update definition', update_definition),
            ('u', 'Update data', update_data),
        ]

        user_data_ = UserData(user_data)
        pick_str_option_ex(f'{user_data_.data_path} action', actions)(user_data_)

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
