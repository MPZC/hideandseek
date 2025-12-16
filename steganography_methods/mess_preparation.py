import base64
import hashlib
import binascii
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

def convertToBinary(message, password, step=None):
    encrypted_message = encryptMessage(message, password)
    # print(f"Kodowanie wiadomości: {message}")
    message = "**" + encrypted_message
    table_of_bin = []
    len_of_message = (len(message)*8)
    # print(len_of_message)
    len_of_message_bin = bin(len_of_message)[2:].zfill(20)
    message_in_binary = len_of_message_bin
    if step:
        if step>1023:
            raise Exception("Zbyt krótka wiadomość")
        step_bin = bin(step)[2:].zfill(10)
        message_in_binary = step_bin + len_of_message_bin

    # Konwersja każdego znaku do formatu binarnego
    for char in message:
        bin_repr = bin(ord(char))[2:].zfill(8)
        table_of_bin.append(bin_repr)

    for b in table_of_bin:
        message_in_binary += b

    return message_in_binary


def convertToString(message_in_binary, password):
    # print(f"Message in binary: {message_in_binary}")
    table_of_strings = []
    message = ""
    for char in range(0, len(message_in_binary), 8):
        table_of_strings.append(chr(int(message_in_binary[char:char+8], 2)))

    for i in table_of_strings:
        message += i
    
    if message[:2] != '**':
        raise ValueError(f"Niepoprawny nagłówek: {message[:10]!r}")
    
    decrypted_message = decryptMessage(message[2:], password)

    return decrypted_message


def generateKeyFromPassword(password, salt, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


def encryptMessage(message, password):
    salt = os.urandom(16)
    key = generateKeyFromPassword(password, salt)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    # Store salt + encrypted data together, base64 encode for transport
    encrypted_out = base64.urlsafe_b64encode(salt + encrypted)
    return encrypted_out.decode()


def decryptMessage(encrypted_message, password):
    encrypted_message += '=' * (-len(encrypted_message) % 4)
    encrypted_data = base64.urlsafe_b64decode(encrypted_message.encode())
    salt = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    key = generateKeyFromPassword(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(ciphertext)
    return decrypted.decode()


