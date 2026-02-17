import os
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# 32 bytes key for AES-256
SECRET_KEY = b'APRRAONJGEACMTEDNECCRRYPPTT16102505'  

def encrypt(plain_text):
    # Generate random 16-byte IV
    iv = os.urandom(16)

    # Pad the plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    # Create Cipher
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # Return IV + encrypted text (Base64 encoded)
    return base64.b64encode(iv + encrypted).decode()


def decrypt(cipher_text):
    # Decode Base64
    cipher_data = base64.b64decode(cipher_text)

    # Extract IV (first 16 bytes)
    iv = cipher_data[:16]
    encrypted = cipher_data[16:]

    # Create Cipher
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt
    padded_plain = decryptor.update(encrypted) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    plain_text = unpadder.update(padded_plain) + unpadder.finalize()

    return plain_text.decode()


# Example Usage
if __name__ == "__main__":
    text = "Hello Arun 🔐"

    encrypted_text = encrypt(text)
    print("Encrypted:", encrypted_text)

    decrypted_text = decrypt(encrypted_text)
    print("Decrypted:", decrypted_text)
