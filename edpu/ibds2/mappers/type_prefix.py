from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE


def type_to_prefix(type_: str) -> str:
    if type_ == TYPE_DIR:
        return 'd'
    elif type_ == TYPE_FILE:
        return 'f'
    else:
        raise Exception()


def prefix_to_type(prefix: str) -> str:
    if prefix == 'd':
        return TYPE_DIR
    elif prefix == 'f':
        return TYPE_FILE
    else:
        raise Exception()
