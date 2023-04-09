from peak_bench import peak_bench

if __name__ == '__main__':
    # HVY-WAP9
    process_count = 12

    # HVY-WAP9 ECO/turbo power profile
    # CPU-PP peaks up to ~48W on turbo power profile
    pack_iterations = 8000
    sleep_between_peaks_time = 6

    peak_bench(process_count, pack_iterations, sleep_between_peaks_time, 'power_manager_abuse_stop')
