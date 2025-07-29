CHKDSK = 'chkdsk'


def chkdsk_cmd(disk: str) -> str:
    return f'{CHKDSK} {disk}:'


def chkdsk_run_multi(disks: str) -> None:
    for disk in disks:
        from .user_interaction import accent_print
        from subprocess import run

        cmd = chkdsk_cmd(disk)

        accent_print([
            f'Preparing to {CHKDSK}...',
            f'disk - {disk}',
            f'cmd - {cmd}',
        ])

        run(cmd)
