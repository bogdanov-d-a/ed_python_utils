from __future__ import annotations
from .location import Location
from typing import Optional


class CollectionData2:
    def __init__(self: CollectionData2, bundle_slices: list[tuple[str, str]], bundle_aliases: list[tuple[str, list[str]]]) -> None:
        self.bundle_slices = bundle_slices
        self.bundle_aliases = bundle_aliases


class Collection:
    def __init__(self: Collection, locations: list[Location], scan_skip_paths: list[str], duplicate_skip_paths: list[str], cd2: Optional[CollectionData2]) -> None:
        self.locations = locations
        self.scan_skip_paths = scan_skip_paths
        self.duplicate_skip_paths = duplicate_skip_paths
        self.cd2 = cd2


CollectionList = list[tuple[str, Collection]]
