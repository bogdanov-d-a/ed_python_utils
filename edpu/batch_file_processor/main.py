from typing import Callable


APP_NAME = 'batch_file_processor'


def _pick_action() -> Callable[[str, str], None]:
    from ..user_interaction import pick_str_option_ex
    from . import order_renamer
    from . import png_to_jpg
    from . import sha1_renamer

    return pick_str_option_ex(f'{APP_NAME} action', [
        ('o', 'order_renamer', order_renamer.exec_),
        ('o2', 'order_renamer name_length=2', lambda a, b: order_renamer.exec_(a, b, name_length=2)),
        ('p', 'png_to_jpg', png_to_jpg.exec_),
        ('p50', 'png_to_jpg quality=50', lambda a, b: png_to_jpg.exec_(a, b, 50)),
        ('s', 'sha1_renamer', sha1_renamer.exec_),
        ('sk', 'sha1_renamer keep_name', lambda a, b: sha1_renamer.exec_(a, b, keep_name=True)),
        ('s8', 'sha1_renamer name_length=8', lambda a, b: sha1_renamer.exec_(a, b, 8)),
        ('s8k', 'sha1_renamer name_length=8 keep_name', lambda a, b: sha1_renamer.exec_(a, b, 8, True)),
    ])


def _pick_path() -> str:
    from ..user_interaction import list_to_dict, pick_str_option
    from edpu_user.batch_file_processor import get_paths

    dict_ = list_to_dict(get_paths())
    return dict_[pick_str_option(f'{APP_NAME} path', dict_)]


def _main() -> None:
    from .utils import path_join
    path_ = _pick_path()
    _pick_action()(path_join(path_, f'{APP_NAME}_src'), path_join(path_, f'{APP_NAME}_dst'))


def run() -> None:
    from edpu import pause_at_end
    pause_at_end.run(_main, pause_at_end.DEFAULT_MESSAGE)
