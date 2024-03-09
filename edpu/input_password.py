def get_and_verify_password(verify_key: bytes, salt: bytes) -> str:
    while True:
        from getpass import getpass
        from hashlib import pbkdf2_hmac

        password = getpass()
        key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        if key == verify_key:
            return password

        print('pbkdf2_hmac key mismatch, got ' + str(key))
