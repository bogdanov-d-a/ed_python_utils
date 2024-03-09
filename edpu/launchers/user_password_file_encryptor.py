if __name__ == '__main__':
    from edpu.user_password_file_encryptor import encrypt
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()

    encrypt(args.file_name)
