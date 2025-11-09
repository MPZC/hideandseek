import heapq
import json
import numpy as np
from PIL import Image
from collections import defaultdict

class Huffman:

    def build_huffman_tree(self, message):
        frequency = defaultdict(int)
        for char in message:
            frequency[char] += 1

        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        huffman_tree = heap[0][1:]
        huffman_codes = {}
        for char, code in huffman_tree:
            huffman_codes[char] = code

        return huffman_codes


    def compress_message(self, message, huffman_codes):
        return ''.join([huffman_codes[char] for char in message])


    def decompress_message(self, binary_message, huffman_codes):
        reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
        current_code = ""
        decoded_message = ""

        for bit in binary_message:
            current_code += bit
            if current_code in reverse_huffman_codes:
                decoded_message += reverse_huffman_codes[current_code]
                current_code = ""

        return decoded_message


    def huffmanCoding(self, img, message):
        shape = img.shape
        size = img.size
        resized_img = img.reshape(-1)
        pixel = 0

        # Huffman coding
        huffman_codes = self.build_huffman_tree(message)
        compressed_message = self.compress_message(message, huffman_codes)
        huffman_json = json.dumps(huffman_codes)
        huffman_bin = ''.join(f"{ord(c):08b}" for c in huffman_json)
        huffman_len_bin = bin(len(huffman_bin))[2:].zfill(20)  # długość słownika

        # Write lenght of huffman table in image
        for bit in huffman_len_bin:
            resized_img[pixel] = np.uint8(resized_img[pixel] & 254 | int(bit))
            pixel += 1

        # Save huuffman table in image
        for bit in huffman_bin:
            resized_img[pixel] = np.uint8(resized_img[pixel] & 254 | int(bit))
            pixel += 1

        # Message and it's lenght in image
        length_in_binary = bin(len(compressed_message))[2:].zfill(20)
        for bit in length_in_binary:
            resized_img[pixel] = np.uint8(resized_img[pixel] & 254 | int(bit))
            pixel += 1
        for bit in compressed_message:
            resized_img[pixel] = np.uint8(resized_img[pixel] & 254 | int(bit))
            pixel += 1

        if pixel > size:
            raise ValueError("The message is too long for this picture")

        new_img = resized_img.reshape(shape)
        pil_image = Image.fromarray(new_img)
        return new_img, pil_image


    def huffmanDecoding(self, img_path):
        img = np.array(Image.open(img_path))
        resized_img = img.reshape(-1)
        pixel = 0

        # Read huffman table and it's lenght
        huffman_len_bin = ""
        for _ in range(20):
            huffman_len_bin += str(resized_img[pixel] & 1)
            pixel += 1
        huffman_len = int(huffman_len_bin, 2)
        huffman_bin = ""
        for _ in range(huffman_len):
            huffman_bin += str(resized_img[pixel] & 1)
            pixel += 1

        huffman_json = ''.join(chr(int(huffman_bin[i:i+8], 2)) for i in range(0, len(huffman_bin), 8))
        huffman_codes = json.loads(huffman_json)

        # Read message lenght and message
        length_in_binary = ""
        for _ in range(20):
            length_in_binary += str(resized_img[pixel] & 1)
            pixel += 1
        message_length = int(length_in_binary, 2)

        compressed_message = ""
        for _ in range(message_length):
            compressed_message += str(resized_img[pixel] & 1)
            pixel += 1

        return compressed_message, huffman_codes


    def decodeMessage(self, stego_path):
        compressed_message, huffman_codes = self.huffmanDecoding(stego_path)
        decoded_message = self.decompress_message(compressed_message, huffman_codes)

        return decoded_message


    def codeMessage(self, path, message):
        img = np.array(Image.open(path))
        _, stego_img = self.huffmanCoding(img, message)
        return stego_img

if __name__ == '__main__':
    huff = Huffman()
    message = 'Hello World!'
    path = 'path_to_img'
    stego_path = 'path_to_stego_img'
    stego_img = huff.codeMessage(path, message)
    stego_img.save(stego_path)
    print("Odkodowana wiadomość:", huff.decodeMessage(stego_path))
