def generate_file(ssid: str, password: str, path: str) -> None:
    with open(path, 'w', encoding='ascii', newline='') as file:
        from .nmcli_device_wifi_connect import nmcli_device_wifi_connect
        from .shebang import SHEBANG_BIN_SH

        file.write(SHEBANG_BIN_SH + '\n')
        file.write(nmcli_device_wifi_connect(ssid, password) + '\n')
