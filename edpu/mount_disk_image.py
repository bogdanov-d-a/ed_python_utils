def mount_disk_image(image_path: str) -> None:
    from .powershell import powershell_command
    from .string_utils import merge_with_space, quotation_mark_wrap

    powershell_command(merge_with_space([
        'Mount-DiskImage',
        '-ImagePath',
        quotation_mark_wrap(image_path),
    ]))


def list_vhds(root: str) -> list[str]:
    from .listdir_helper import listdir_helper, TYPE_FILE
    from os.path import splitext

    return sorted(filter(
        lambda name: splitext(name)[1] == '.vhd',
        listdir_helper(root)[TYPE_FILE]
    ))


def run_interactive() -> None:
    from .user_interaction import pick_str_option_ex

    def dir(root: str) -> None:
        from .user_interaction import yes_no_prompt
        from os.path import join

        vhds = list(map(
            lambda vhd: join(root, vhd),
            list_vhds(root)
        ))

        if yes_no_prompt(f'mount {vhds}'):
            for vhd in vhds:
                mount_disk_image(vhd)

    pick_str_option_ex('mount_disk_image run_interactive', [
        ('s', 'single', lambda: mount_disk_image(input())),
        ('d', 'dir', lambda: dir(input())),
        ('f', 'drive', lambda: dir(f'{input().upper()}:\\')),
    ])()
