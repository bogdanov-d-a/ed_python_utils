def _files() -> None:
    from os import getenv
    from os.path import isdir
    from shutil import rmtree

    path = fr'{getenv("APPDATA")}\HeidiSQL'

    if isdir(path):
        rmtree(path)


def _reg() -> None:
    import winreg

    root_path = r'SOFTWARE\HeidiSQL'
    servers_name = 'Servers'
    servers_path = fr'{root_path}\{servers_name}'

    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    root_key = winreg.OpenKey(reg, root_path, access=winreg.KEY_ALL_ACCESS)

    def clean_root() -> None:
        from edpu.win_reg import enum_value

        for n in list(filter(
            lambda n: n.startswith('SQLFile') or n in [
                'ExportSQL_Filenames',
                'FindDialogSearchHistory',
                'GridExportFilename',
                'GridExportRecentFiles',
            ],
            map(
                lambda v: v[0],
                enum_value(root_key)
            )
        )):
            winreg.DeleteValue(root_key, n)

    clean_root()

    def clean_servers() -> None:
        def check() -> bool:
            from edpu.win_reg import enum_key

            keys = list(enum_key(root_key))

            if len(keys) != 1:
                print(keys)

            return servers_name in keys

        if check():
            from edpu.win_reg import enum_key

            servers_key = winreg.OpenKey(reg, servers_path)

            for servers_key_key in list(enum_key(servers_key)):
                def clean() -> None:
                    server_path = fr'{servers_path}\{servers_key_key}'
                    server_key = winreg.OpenKey(reg, server_path)

                    for server_key_key in list(enum_key(server_key)):
                        from edpu.win_reg import reg_delete
                        reg_delete(fr'HKCU\{server_path}\{server_key_key}')

                clean()

    clean_servers()


def main() -> None:
    _files()
    _reg()


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
