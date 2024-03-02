from edpu.mapper import Mapper


def _get_mapper() -> Mapper[str, bool]:
    from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE

    return Mapper([
        (TYPE_DIR, False),
        (TYPE_FILE, True),
    ])


_mapper = _get_mapper()


type_to_isfile = _mapper.fwd
isfile_to_type = _mapper.rev
