DataElem = tuple[str, str, str, str]
DataList = list[DataElem]


def run(data: DataList) -> None:
    from . import pause_at_end

    def get_pick_data() -> list[tuple[str, str, tuple[str, str, str]]]:
        def get_description(e: DataElem) -> str:
            from .string_utils import merge_with_space, quotation_mark_wrap
            return merge_with_space(list(map(quotation_mark_wrap, e[1:])))

        return list(map(
            lambda e: (e[0], get_description(e), e[1:]),
            data
        ))

    def main() -> None:
        from .pack_unpack_action_picker import pick_action
        from .tar_zst_utils import print_and_check_path, TAR_ZST_EXT, pack_tar_zst, unpack_tar_zst, run_with_prompt
        from .user_interaction import pick_str_option_ex

        picked_data = pick_str_option_ex('Pick data', get_pick_data())

        data_path_root = picked_data[0]
        data_path = data_path_root + '\\' + picked_data[1]
        archive_path = picked_data[2]

        print_and_check_path(data_path)
        print_and_check_path(archive_path + TAR_ZST_EXT)

        is_pack = pick_action()
        cmd = pack_tar_zst(data_path, archive_path) if is_pack else unpack_tar_zst(archive_path, data_path_root)
        run_with_prompt(cmd)

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
