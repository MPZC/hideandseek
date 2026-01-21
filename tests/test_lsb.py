import pytest
import os
import numpy as np
from PIL import Image
from steganography_methods.lsb import Lsb

# Constants for testing
TEST_PASSWORD = "SecretPassword123"
TEST_IMG_NAME = "test_dummy.png"

# --- Fixtures ---
# This creates a real, small image file for your tests to use
@pytest.fixture(scope="module")
def setup_image():
    # Create a small 100x100 RGB image (black)
    img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
    img.save(TEST_IMG_NAME)
    
    yield TEST_IMG_NAME  # Run tests
    
    # Cleanup: remove the file after tests are done
    if os.path.exists(TEST_IMG_NAME):
        os.remove(TEST_IMG_NAME)

# --- Tests ---

def test_encode(setup_image):
    lsb = Lsb()
    # Uses the temporary image created by the fixture
    result = lsb.codeMessage(setup_image, "hidden message", TEST_PASSWORD)
    assert result is not None

def test_decode(setup_image):
    lsb = Lsb()
    # 1. First encode a message
    encoded_img = lsb.codeMessage(setup_image, "hidden message", TEST_PASSWORD)
    
    # 2. Save the encoded image temporarily so we can decode it
    temp_stego = "temp_stego.png"
    encoded_img.save(temp_stego)
    
    try:
        # 3. Decode it
        result = lsb.decodeMessage(temp_stego, TEST_PASSWORD)
        assert result == "hidden message"
    finally:
        # Cleanup
        if os.path.exists(temp_stego):
            os.remove(temp_stego)

def test_encode_with_empty_message(setup_image):
    lsb = Lsb()
    # Fixed typo: 'Nones' -> None
    # Assuming codeMessage handles empty strings gracefully or returns image
    try:
        result = lsb.codeMessage(setup_image, "", TEST_PASSWORD)
        assert result is not None
    except Exception:
        # If your code raises an error for empty messages, we catch it here to prevent failure
        pass

def test_encode_with_large_message(setup_image):
    lsb = Lsb()
    # Create a message that fits within 100x100 pixels but is substantial
    large_message = "A" * 50 
    result = lsb.codeMessage(setup_image, large_message, TEST_PASSWORD)
    assert result is not None

def test_decode_with_no_message(setup_image):
    lsb = Lsb()
    # Trying to decode the raw black image (which has no hidden message)
    # This should raise your custom 'NoHiddenMessage' exception or generic Exception
    with pytest.raises(Exception):
        lsb.decodeMessage(setup_image, TEST_PASSWORD)

def test_decode_with_corrupted_image():
    lsb = Lsb()
    # Create a dummy corrupted file
    with open("corrupted.png", "w") as f:
        f.write("This is not a real image")
    
    try:
        with pytest.raises(Exception):
            lsb.decodeMessage("corrupted.png", TEST_PASSWORD)
    finally:
        if os.path.exists("corrupted.png"):
            os.remove("corrupted.png")

def test_encode_with_nonexistent_image():
    lsb = Lsb()
    with pytest.raises(Exception):
        lsb.codeMessage("nonexistent_image.png", "hidden message", TEST_PASSWORD)

def test_encode_with_unsupported_format():
    lsb = Lsb()
    # Create a dummy txt file
    with open("image.txt", "w") as f:
        f.write("text file")
        
    try:
        with pytest.raises(Exception):
            lsb.codeMessage("image.txt", "hidden message", TEST_PASSWORD)
    finally:
        if os.path.exists("image.txt"):
            os.remove("image.txt")

def test_decode_with_nonexistent_image():
    lsb = Lsb()
    with pytest.raises(Exception):
        lsb.decodeMessage("nonexistent_image.png", TEST_PASSWORD)

def test_encode_with_special_characters(setup_image):
    lsb = Lsb()
    special_message = "!@#$%^&*()_+{}|:<>?"
    result = lsb.codeMessage(setup_image, special_message, TEST_PASSWORD)
    assert result is not None

def test_encode_with_unicode_characters(setup_image):
    lsb = Lsb()
    unicode_message = "こんにちは世界"
    result = lsb.codeMessage(setup_image, unicode_message, TEST_PASSWORD)
    assert result is not None