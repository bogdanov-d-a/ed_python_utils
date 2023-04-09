class MultiprocessingCore:
    def __init__(self, process_count, target, args):
        from multiprocessing import Process

        self._processes = []

        for _ in range(process_count):
            self._processes.append(Process(target=target, args=args))

    def start(self):
        for process in self._processes:
            process.start()

    def join(self):
        for process in self._processes:
            process.join()
