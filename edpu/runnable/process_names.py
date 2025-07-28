if __name__ == '__main__':
    from edpu.psutil_helpers import process_names

    for process_name in sorted(process_names()):
        print(process_name)
