from cryptography.fernet import Fernet
from django.conf import settings

# Generate a key (keep it secret and do not hardcode it in production)
key = Fernet.generate_key()

print(key)
def encrypt_data(data):
    cipher_suite = Fernet('nip3ZHDEm5MPvzP0-0-fDyTjiyHIG1xpwy-JJ3yjqd0=')
    if isinstance(data,list):
        encrypted_data = [cipher_suite.encrypt(str(item).encode()) for item in data]
    else:
        encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    cipher_suite = Fernet('nip3ZHDEm5MPvzP0-0-fDyTjiyHIG1xpwy-JJ3yjqd0=')
    plain_text = cipher_suite.decrypt(encrypted_data).decode()
    return plain_text
