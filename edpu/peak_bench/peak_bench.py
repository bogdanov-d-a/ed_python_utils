def peak_bench(process_count, pack_iterations, sleep_between_peaks_time, stop_file_name):
    from .stop_strategy_core import StopStrategyCore

    stop_strategy = StopStrategyCore(stop_file_name)

    while not stop_strategy.need_stop():
        from .bench_core import bench
        from .multiprocessing_core import MultiprocessingCore
        from time import sleep

        multiprocessing = MultiprocessingCore(process_count, bench, [pack_iterations])

        try:
            multiprocessing.start()
            print('started')

        finally:
            multiprocessing.join()
            print('joined')

        if stop_strategy.need_stop():
            break

        sleep(sleep_between_peaks_time)
