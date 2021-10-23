import getpass
import hashlib

def get_and_verify_password(verify_key, salt):
    while True:
        password = getpass.getpass()
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        if key == verify_key:
            return password
        print('pbkdf2_hmac key mismatch, got ' + str(key))
