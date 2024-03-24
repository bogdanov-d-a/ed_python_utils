def _files() -> None:
    from edpu.del_cmd import del_f_q
    from os import system

    recent = r'%APPDATA%\Microsoft\Windows\Recent'

    system(del_f_q(fr'{recent}\*'))
    system(del_f_q(fr'{recent}\AutomaticDestinations\*'))
    system(del_f_q(fr'{recent}\CustomDestinations\*'))


def _reg() -> None:
    from edpu.win_reg import reg_delete

    shell = r'HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell'
    explorer = r'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer'

    reg_delete(fr'{shell}\BagMRU')
    reg_delete(fr'{shell}\Bags')
    reg_delete(fr'{shell}\MuiCache')

    reg_delete(fr'{explorer}\CIDOpen')
    reg_delete(fr'{explorer}\CIDSave')
    reg_delete(fr'{explorer}\ComDlg32')
    reg_delete(fr'{explorer}\DriveIcons')
    reg_delete(fr'{explorer}\Modules\GlobalSettings\Sizer')
    reg_delete(fr'{explorer}\Modules\NavPane')
    reg_delete(fr'{explorer}\RunMRU')
    reg_delete(fr'{explorer}\Streams\Defaults')
    reg_delete(fr'{explorer}\TypedPaths')


def main() -> None:
    from edpu.explorer_lifecycle import ExplorerDown
    from os import system

    with ExplorerDown():
        _files()
        _reg()

    system('rundll32 InetCpl.cpl,ClearMyTracksByProcess 1')


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
