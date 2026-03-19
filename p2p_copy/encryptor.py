import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants for encryption
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
ITERATIONS = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from a password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(input_path: str, output_path: str, password: str):
    """Encrypt a file using AES-256-GCM and save to output_path."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    with open(input_path, 'rb') as f:
        data = f.read()

    # Encrypt data and get authentication tag (combined in AESGCM)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    # Write [SALT][NONCE][CIPHERTEXT]
    with open(output_path, 'wb') as f:
        f.write(salt)
        f.write(nonce)
        f.write(ciphertext)

def decrypt_file(input_path: str, output_path: str, password: str):
    """Decrypt a file using AES-256-GCM and save to output_path."""
    with open(input_path, 'rb') as f:
        salt = f.read(SALT_SIZE)
        nonce = f.read(NONCE_SIZE)
        ciphertext = f.read()

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
    except Exception as e:
        raise ValueError("Decryption failed. Incorrect password or corrupted data.") from e

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
