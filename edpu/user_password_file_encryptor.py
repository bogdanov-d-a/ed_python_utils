import argparse
from edpu import file_encryptor
from edpu_user import password_provider

def encrypt(file_name: str) -> None:
    file_encryptor.encrypt(file_name, password_provider.get(), file_name + '.7z')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()
    encrypt(args.file_name)
