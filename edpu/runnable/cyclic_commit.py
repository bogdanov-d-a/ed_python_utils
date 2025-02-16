if __name__ == '__main__':
    from edpu.cyclic_commit import cyclic_commit
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()

    cyclic_commit(args.path)
