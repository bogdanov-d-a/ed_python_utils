class Remotes:
    def __init__(self, native):
        self.native = native

class Data:
    def __init__(self, host_to_path, remotes):
        self.host_to_path = host_to_path
        self.remotes = remotes
