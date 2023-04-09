import os.path

class StopStrategyCore:
    def __init__(self, file_name):
        self._file_name = file_name

    def need_stop(self):
        return os.path.isfile(self._file_name)
