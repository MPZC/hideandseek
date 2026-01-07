# HideAndSeek 🕵️‍♂️🖼️

**HideAndSeek** is a modern web application for steganography – the art of hiding information. The application allows you to securely embed secret text messages inside PNG image files using advanced bit‑manipulation techniques and strong encryption.

## 🚀 Features

* **Message Hiding (Encoding):** Embed a secret text inside a PNG image so that it is invisible to the human eye.

* **Message Extraction (Decoding):** Retrieve the hidden content from an image if you know the password.

* **Encryption:** Each message is encrypted (AES/Fernet) before being hidden in the image. Without the correct passphrase, the message is impossible to read, even if someone extracts the raw bits.

* **3 Steganographic Methods:** Choose the algorithm that best suits your needs (LSB, Huffman, Random LSB).

* **Modern Interface:** Dark Mode, responsive design, and intuitive user experience.

## 🛠️ Technologies

The project is built using:

* **Backend:** Python 3, Flask

* **Image Processing:** Pillow (PIL), NumPy

* **Cryptography:** `cryptography` library (Fernet / PBKDF2HMAC)

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)

## 🧠 Implemented Algorithms

The application offers three data‑hiding methods:

1. **LSB (Least Significant Bit):**

   * A classic technique that replaces the least significant bit of each pixel with a message bit.
   * The message is embedded sequentially.

2. **Random LSB:**

   * A more discreet approach. It calculates a “step” (spacing) based on the image size and message length.
   * Message bits are distributed across the entire image instead of being concentrated at the beginning.

3. **Huffman Coding:**

   * Compresses the message before embedding using Huffman coding.
   * Allows more text to be hidden with less impact on the image (fewer pixel changes).
   * Stores the Huffman tree structure in the image header.

## ⚙️ Installation and Running

To run the project locally, follow the steps below:

### Requirements

* Python 3.8+
* pip

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MPZC/hideandseek
   cd HideAndSeek
   ```

2. **Recommended: Create a virtual environment:**

   ```bash
   python -m venv .
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python app.py
   ```

5. **Open in your browser:**
   Go to: `http://localhost:8080`

## 📖 User Guide

### Encoding (Hiding a Message)

1. Make sure the mode switch is set to **Encode**.
2. Select an image file (`.png`, max 5MB).
3. Choose an encoding method (e.g. LSB).
4. Enter the secret message.
5. Set a strong passphrase.
6. Click **Encode**. After success, download the generated image (`stego_image.png`).

### Decoding (Extracting a Message)

1. Switch the mode to **Decode** (toggle in the top menu).
2. Upload the image containing the hidden message.
3. Select the same method that was used for encoding.
4. Enter the passphrase used during encoding.
5. Click **Decode**. If the data is correct, the message will be displayed on the screen.

