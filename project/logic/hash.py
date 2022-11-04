import hashlib


def hash_password(password):
    hashpassword = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashpassword
