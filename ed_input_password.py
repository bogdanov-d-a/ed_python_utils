import getpass
import hashlib

def get_and_verify_password(verify_sha1):
    while True:
        password = getpass.getpass()
        sha1 = hashlib.sha1()
        sha1.update(password.encode('utf-8'))
        user_sha1 = sha1.hexdigest()
        if user_sha1 == verify_sha1:
            return password
        print('SHA1 mismatch, got ' + user_sha1)
