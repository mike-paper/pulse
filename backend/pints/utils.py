import os
from cryptography.fernet import Fernet

FERNET_KEY = os.environ.get('PAPER_FERNET_KEY')

def encrypt(e):
    f = Fernet(FERNET_KEY)
    e = e.encode("utf-8")
    return f.encrypt(e).decode()

def decrypt(d):
    f = Fernet(FERNET_KEY)
    d = f.decrypt(d.encode("utf-8"))
    return d.decode()