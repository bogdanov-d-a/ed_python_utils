from edpu import host_alias
from edpu import storage_finder
from ed_ibds.storage_device import StorageDevice
from ed_ibds.location import Location
from ed_ibds.user_data import UserData
from ed_ibds import main_app
import os


_PC = 'PC'
_Laptop = 'Laptop'
_USBFlash = 'USBFlash'

_DEVICES = set([_PC, _Laptop, _USBFlash])
_DEVICES_REMOVABLE = set([_USBFlash])


host_alias_ = host_alias.get()
all_storage = storage_finder.find_all_storage()

def create_device(name):
    if name not in _DEVICES:
        raise Exception('Bad device name')
    return StorageDevice(name, name in _DEVICES_REMOVABLE, (name in _DEVICES_REMOVABLE and name in all_storage) or name == host_alias_)

devices = []
for name in _DEVICES:
    devices.append(create_device(name))


collection_dict = {
    'Music': ([
        Location(create_device('PC'), 'C:\\Users\\Username\\Music', True),
        Location(create_device('Laptop'), 'C:\\Users\\Username\\Music', True),
        Location(create_device('USBFlash'), 'Music', False),
    ], [], []),
    'Pictures': ([
        Location(create_device('PC'), 'C:\\Users\\Username\\Pictures', True),
        Location(create_device('Laptop'), 'C:\\Users\\Username\\Pictures', True),
        Location(create_device('USBFlash'), 'Pictures', True),
    ], [
        r'^.*Thumbs\.db$',
    ], []),
}


data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
main_app.run(UserData(collection_dict, devices, data_path, True, True))
