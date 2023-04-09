from os.path import isfile

class StopStrategyCore:
    def __init__(self, file_name):
        self._file_name = file_name

    def need_stop(self):
        return isfile(self._file_name)
