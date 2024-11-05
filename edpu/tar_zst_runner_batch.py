from __future__ import annotations


class App:
    def __init__(self: App, source_dirs_raw: str, out_dir: str, is_pack: bool) -> None:
        self._sources = list(map(
            lambda source_dir: (source_dir, App.get_name_for_source_dir(source_dir)),
            source_dirs_raw.split('\n')
        ))

        App.check_duplicates(list(map(lambda source: source[0], self._sources)), 'paths')
        App.check_duplicates(list(map(lambda source: source[1], self._sources)), 'names')

        self._out_dir = out_dir
        self._is_pack = is_pack


    def run(self: App) -> None:
        for source in self._sources:
            from .tar_zst_utils import print_and_check_path, TAR_ZST_EXT, run_with_prompt

            out_path = self._out_dir + source[1]

            print_and_check_path(source[0])
            print_and_check_path(out_path + TAR_ZST_EXT)

            if self._is_pack:
                from .tar_zst_utils import pack_tar_zst
                cmd = pack_tar_zst(source[0], out_path)
            else:
                from .tar_zst_utils import unpack_tar_zst
                from os.path import split
                cmd = unpack_tar_zst(out_path, split(source[0])[0])

            run_with_prompt(cmd)


    @staticmethod
    def get_name_for_source_dir(source_dir: str) -> str:
        return source_dir \
            .replace('C:\\', '') \
            .replace('\\', '_') \
            .replace('.', '_') \
            .replace(' ', '_')


    @staticmethod
    def check_duplicates(list_: list[str], name: str) -> None:
        if len(list_) != len(set(list_)):
            raise Exception('check_duplicates failed for ' + name)


def run(source_dirs_raw: str, out_dir: str) -> None:
    from . import pause_at_end
    from .pack_unpack_action_picker import pick_action

    pause_at_end.run(
        lambda: App(source_dirs_raw, out_dir, pick_action()).run(),
        pause_at_end.DEFAULT_MESSAGE
    )
