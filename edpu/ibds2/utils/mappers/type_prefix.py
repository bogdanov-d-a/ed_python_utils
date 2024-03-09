from ....mapper import Mapper


def _get_mapper() -> Mapper[str, str]:
    from ....file_tree_walker import TYPE_DIR, TYPE_FILE

    return Mapper([
        (TYPE_DIR, 'd'),
        (TYPE_FILE, 'f'),
    ])


_mapper = _get_mapper()


type_to_prefix = _mapper.fwd
prefix_to_type = _mapper.rev
