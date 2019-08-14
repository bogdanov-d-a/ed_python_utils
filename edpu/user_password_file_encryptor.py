import argparse
import edpu.file_encryptor
import edpu.user.password_provider

def encrypt(file_name):
    edpu.file_encryptor.encrypt(file_name, edpu.user.password_provider.get(), file_name + '.7z')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()
    encrypt(args.file_name)
