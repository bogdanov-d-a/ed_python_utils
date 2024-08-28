from .device import Device


def map_device_names(devices: list[Device]) -> list[str]:
    return list(map(
        lambda device: device.name,
        devices
    ))


def filter_removable_devices(devices: list[Device]) -> list[Device]:
    return list(filter(
        lambda device: device.is_removable,
        devices
    ))
