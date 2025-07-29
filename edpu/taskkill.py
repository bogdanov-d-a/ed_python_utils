TASKKILL = 'taskkill'
TASKKILL_FORCE = '/f'

TASKKILL_TYPE_PROCESS_ID = '/pid'
TASKKILL_TYPE_IMAGE = '/im'


def taskkill(type: str, value: str, force: bool=False) -> None:
    data = [TASKKILL]

    if force:
        data.append(TASKKILL_FORCE)

    data += [
        type,
        value,
    ]

    from subprocess import run
    print(f'taskkill returncode: {run(data).returncode}')


def taskkill_image(name: str, force: bool=False) -> None:
    taskkill(TASKKILL_TYPE_IMAGE, name, force)
