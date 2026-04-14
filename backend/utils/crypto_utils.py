import os
import secrets
from binascii import unhexlify, hexlify
from cryptography.hazmat.primitives import hashes, hmac, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidSignature
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

def _get_key():
    """
    Retrieves the AES key from the environment and converts it from hex to bytes.
    """
    hex_key = os.getenv("AES_KEY")
    if not hex_key:
        raise ValueError("AES_KEY not found in environment.")
    return unhexlify(hex_key)

def _get_hmac_key():
    """
    Retrieves the HMAC key from the environment and converts it from hex to bytes.
    """
    hex_key = os.getenv("HMAC_KEY")
    if not hex_key:
        raise ValueError("HMAC_KEY not found in environment.")
    return unhexlify(hex_key)

def encrypt(plaintext: str) -> str:
    """
    Encrypts a string using AES-CBC (with PKCS7 padding) and returns a hex-encoded string of (IV + ciphertext).
    """
    key = _get_key()
    iv = secrets.token_bytes(16) # AES block size is 16 bytes
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    # 1. Apply PKCS7 padding
    padder = padding.PKCS7(128).padder() # 128 bit block size for AES
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    
    # 2. Encrypt
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # 3. Prepend IV to ciphertext and hex-encode
    return hexlify(iv + ciphertext).decode()

def decrypt(encrypted_hex: str) -> str:
    """
    Decrypts a hex-encoded string (containing IV + ciphertext) using AES-CBC.
    """
    key = _get_key()
    try:
        data = unhexlify(encrypted_hex)
        if len(data) < 17:
            raise ValueError("Encrypted data is too short.")
            
        iv = data[:16]
        ciphertext = data[16:]
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        # 1. Decrypt
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # 2. Remove PKCS7 padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode()
    except Exception as e:
        return f"Error during decryption: {str(e)}"

def sign(data_to_sign: str) -> str:
    """Signs data string using HMAC-SHA256 and returns a hex-encoded signature."""
    key = _get_hmac_key()
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data_to_sign.encode())
    return hexlify(h.finalize()).decode()

def verify(data_to_verify: str, signature_hex: str) -> bool:
    """Verifies HMAC-SHA256 signature for data string. Returns True if valid."""
    key = _get_hmac_key()
    try:
        h = hmac.HMAC(key, hashes.SHA256())
        h.update(data_to_verify.encode())
        h.verify(unhexlify(signature_hex))
        return True
    except (InvalidSignature, ValueError, Exception):
        return False