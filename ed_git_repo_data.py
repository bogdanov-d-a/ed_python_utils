class Remotes:
    def __init__(self, native, storage):
        self.native = native
        self.storage = storage

class Data:
    def __init__(self, host_to_path, remotes, branches, bundle_versions):
        self.host_to_path = host_to_path
        self.remotes = remotes
        self.branches = branches
        self.bundle_versions = bundle_versions
