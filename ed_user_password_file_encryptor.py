import argparse
import ed_file_encryptor
import ed_user_password_provider

def encrypt(file_name):
    ed_file_encryptor.encrypt(file_name, ed_user_password_provider.get(), file_name + '.7z')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()
    encrypt(args.file_name)
