from peak_bench import peak_bench

if __name__ == '__main__':
    # HVY-WAP9
    process_count = 6

    # HVY-WAP9 ECO power profile
    pack_iterations = 250
    sleep_between_peaks_time = 0.1

    peak_bench(process_count, pack_iterations, sleep_between_peaks_time, 'power_manager_flat_stop')
