def nmcli_device_wifi_connect(ssid: str, password: str) -> str:
    return f'nmcli device wifi connect {ssid} password {password}'
