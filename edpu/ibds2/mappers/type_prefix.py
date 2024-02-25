from edpu.file_tree_walker import TYPE_DIR, TYPE_FILE
from edpu.mapper import Mapper


_mapper = Mapper([
    (TYPE_DIR, 'd'),
    (TYPE_FILE, 'f'),
])


type_to_prefix = _mapper.fwd
prefix_to_type = _mapper.rev
