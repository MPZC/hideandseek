import pytest
from steganography_methods.lsb import encode, decode

def test_encode():
    # Example test for encode function
    result = encode("image.png", "hidden message")
    assert result is not None

def test_decode():
    # Example test for decode function
    result = decode("image_with_message.png")
    assert result == "hidden message"

def test_encode_with_empty_message():
    # Test encoding with an empty message
    result = encode("image.png", "")
    assert result is not Nones

def test_encode_with_large_message():
    # Test encoding with a large message
    large_message = "A" * 10000  # Example large message
    result = encode("image.png", large_message)
    assert result is not None

def test_decode_with_no_message():
    # Test decoding an image with no hidden message
    result = decode("image_without_message.png")
    assert result == ""

def test_decode_with_corrupted_image():
    # Test decoding a corrupted image
    with pytest.raises(Exception):
        decode("corrupted_image.png")

def test_encode_with_nonexistent_image():
    # Test encoding with a nonexistent image file
    with pytest.raises(FileNotFoundError):
        encode("nonexistent_image.png", "hidden message")

def test_encode_with_unsupported_format():
    # Test encoding with an unsupported image format
    with pytest.raises(ValueError):
        encode("image.txt", "hidden message")

def test_decode_with_nonexistent_image():
    # Test decoding a nonexistent image file
    with pytest.raises(FileNotFoundError):
        decode("nonexistent_image.png")

def test_decode_with_unsupported_format():
    # Test decoding an unsupported image format
    with pytest.raises(ValueError):
        decode("image.txt")

def test_encode_with_special_characters():
    # Test encoding a message with special characters
    special_message = "!@#$%^&*()_+{}|:<>?"
    result = encode("image.png", special_message)
    assert result is not None

def test_encode_with_unicode_characters():
    # Test encoding a message with Unicode characters
    unicode_message = "こんにちは世界"  # "Hello, World" in Japanese
    result = encode("image.png", unicode_message)
    assert result is not None

def test_decode_with_special_characters():
    # Test decoding a message with special characters
    result = decode("image_with_special_message.png")
    assert result == "!@#$%^&*()_+{}|:<>?"

def test_decode_with_unicode_characters():
    # Test decoding a message with Unicode characters
    result = decode("image_with_unicode_message.png")
    assert result == "こんにちは世界"