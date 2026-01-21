import pytest
from steganography_methods.mess_preparation import (
    encryptMessage, 
    decryptMessage, 
    convertToBinary, 
    convertToString,
    generateKeyFromPassword
)
from exceptions import InvalidPassword

# Constants
TEST_PASSWORD = "StrongPassword123!"
WRONG_PASSWORD = "WrongPassword"
TEST_MESSAGE = "Secret Message"

# --- Encryption & Decryption Tests ---

def test_encrypt_decrypt_flow():
    """Verify that a message can be encrypted and then decrypted back to original."""
    encrypted = encryptMessage(TEST_MESSAGE, TEST_PASSWORD)
    decrypted = decryptMessage(encrypted, TEST_PASSWORD)
    assert decrypted == TEST_MESSAGE

def test_decrypt_with_wrong_password():
    """Verify that decoding with the wrong password raises InvalidPassword."""
    encrypted = encryptMessage(TEST_MESSAGE, TEST_PASSWORD)
    
    with pytest.raises(InvalidPassword):
        decryptMessage(encrypted, WRONG_PASSWORD)

def test_decrypt_corrupted_data():
    """Verify that decoding nonsense data raises InvalidPassword (or generic error)."""
    corrupted_data = "NotAnEncryptedString"
    
    with pytest.raises(InvalidPassword):
        decryptMessage(corrupted_data, TEST_PASSWORD)

def test_encryption_is_randomized():
    """
    Verify that encrypting the same message twice results in different outputs
    (due to random salt generation).
    """
    enc1 = encryptMessage(TEST_MESSAGE, TEST_PASSWORD)
    enc2 = encryptMessage(TEST_MESSAGE, TEST_PASSWORD)
    assert enc1 != enc2

# --- Binary Conversion Tests ---

def test_convert_to_binary_structure():
    """
    Test if convertToBinary produces a binary string.
    The output structure is: [20-bit length] + [binary data of '**' + encrypted_msg]
    """
    binary_out = convertToBinary(TEST_MESSAGE, TEST_PASSWORD)
    
    # Must be a string of 0s and 1s
    assert all(c in '01' for c in binary_out)
    
    # The first 20 bits should represent the length of the payload
    length_header = binary_out[:20]
    payload = binary_out[20:]
    
    # Calculate expected length from the binary payload
    payload_len = len(payload)
    header_val = int(length_header, 2)
    
    assert payload_len == header_val

def test_convert_to_string_flow():
    """Full cycle: String -> Binary -> String."""
    binary_out = convertToBinary(TEST_MESSAGE, TEST_PASSWORD)
    decoded_msg = convertToString(binary_out[20:], TEST_PASSWORD) # convertToString expects JUST the payload, not the length header?
    
    # Wait, looking at your code for `convertToString`:
    # It takes `message_in_binary` and loops over it in chunks of 8.
    # It does NOT seem to expect the 20-bit length header inside the argument.
    # However, `lsb.py` or `huffman.py` usually handle the length stripping before calling this.
    # So we pass only the payload part here.
    
    assert decoded_msg == TEST_MESSAGE

def test_convert_to_string_invalid_header():
    """
    If the binary data decodes to a string that doesn't start with '**',
    it should raise ValueError.
    """
    # Create a binary string for "BadHeader" (missing the '**' prefix)
    bad_msg = "BadHeader" + "junkdata"
    # Convert manually to binary
    bad_binary = ''.join(format(ord(c), '08b') for c in bad_msg)
    
    with pytest.raises(ValueError, match="Niepoprawny nagłówek"):
        convertToString(bad_binary, TEST_PASSWORD)

def test_convert_to_binary_with_step():
    """Test the optional 'step' parameter functionality."""
    step = 5
    binary_out = convertToBinary(TEST_MESSAGE, TEST_PASSWORD, step=step)
    
    # Structure with step: [10-bit step] + [20-bit length] + [payload]
    
    # 1. Check Step Header (first 10 bits)
    step_header = binary_out[:10]
    assert int(step_header, 2) == step
    
    # 2. Check Length Header (next 20 bits)
    length_header = binary_out[10:30]
    payload = binary_out[30:]
    assert len(payload) == int(length_header, 2)

def test_convert_to_binary_step_too_large():
    """Verify exception when step > 1023."""
    with pytest.raises(Exception, match="Zbyt krótka wiadomość"):
        convertToBinary(TEST_MESSAGE, TEST_PASSWORD, step=1024)

# --- Special Characters ---

def test_special_chars_encryption():
    """Test with Unicode characters and emojis."""
    special_msg = "Zażółć gęślą jaźń 🚀"
    
    # Encrypt -> Decrypt
    enc = encryptMessage(special_msg, TEST_PASSWORD)
    dec = decryptMessage(enc, TEST_PASSWORD)
    assert dec == special_msg
    
    # Binary Cycle
    binary_out = convertToBinary(special_msg, TEST_PASSWORD)
    # Strip 20-bit length header for convertToString
    decoded = convertToString(binary_out[20:], TEST_PASSWORD)
    assert decoded == special_msg