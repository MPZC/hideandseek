"""
Ten skrypt implementuje klasyczną metodę ukrywania wiadomości w obrazach przy użyciu algorytmu LSB (Least Significant Bit).
Koduje wiadomość w ostatnich bitach pikseli obrazu, a następnie umożliwia jej odkodowanie.

Moduły:
- `convertImage`  Konwertuje obraz na macierz numpy do manipulacji pikselami.
- `lsbCoding`  Ukrywa binarną wiadomość w ostatnich bitach pikseli obrazu.
- `lsbDecoding`  Odczytuje ukrytą wiadomość z obrazu.
"""

import numpy as np
from PIL import Image
from mess_preparation import convertToBinary, convertToString

class Lsb:
    # Konwertuje obraz do macierzy numpy w celu manipulacji pikselami
    def convertImage(self, path):
        img = Image.open(path)
        numpy_img = np.array(img)
        return img, numpy_img


    '''Koduje wiadomość w obrazie poprzez zastąpienie ostatnich bitów pikseli obrazem binarnej wiadomości.
    Zwraca:
    1. Zakodowany obraz w formacie numpy
    2. Zakodowany obraz w formacie PIL (do zapisu)
    '''
    def lsbCoding(self, img, message):
        shape = img.shape     # Kształt obrazu
        size = img.size       # Rozmiar obrazu
        resized_img = img.reshape(size)  # Zmienia macierz obrazu, aby była była jednowymiarowa
        pixel = 0             # Zmienna kontrolująca przesuwanie się po pikselach 
        for bit in range(0, len(message)-1):
            if bit >= len(resized_img):
                new_img = resized_img.reshape(shape)
                pil_image = Image.fromarray(new_img)
                return new_img, pil_image
            if message[bit] == '0':
                resized_img[pixel] = resized_img[pixel] & ~1  # Wyzerowanie ostatniego bitu
            elif message[bit] == '1':
                resized_img[pixel] = resized_img[pixel] | 1   # Ustawienie ostatniego bitu na 1
            else:
                print("Błąd")
            pixel += 1

        new_img = resized_img.reshape(shape)
        pil_image = Image.fromarray(new_img)
        return new_img, pil_image


    '''Odczytuje zakodowaną wiadomość z obrazu, czytając ostatnie bity pikseli.
    Zwraca:
    - Wiadomość w postaci binarnej.
    '''
    def lsbDecoding(self, img_path):
        _, img = self.convertImage(img_path)
        message = ''
        resized_img = img.reshape(1, img.size)
        size_of_text = ''

        # Odczyt wiadomości z pikseli
        for bit in range(0, 20):      # (2, 149, 3) - jeżeli chcemy zakodować wiadomość tylko w pikselach B (blue), wtedy należy zmeinić też pętlę poniżej (2, (size*3)+2, 3), a rakże w funkcji coding
            if resized_img[0, bit] % 2 == 0:
                size_of_text += '0'
            elif resized_img[0, bit] % 2 == 1:
                size_of_text += '1'
            else:
                print("Błąd")
        size = int(size_of_text, 2)
        # print(size)

        # Odczyt ukrytej wiadomości
        for bit in range(20, 20 + size):
            if resized_img[0, bit] % 2 == 0:
                message += '0'
            elif resized_img[0, bit] % 2 == 1:
                message += '1'
            else:
                print("Błąd")
        return message


    def codeMessage(self, path, message, password):
        message_in_binary = convertToBinary(message, password)
        _, img = self.convertImage(path)
        if len(message_in_binary) > (img.size):
            raise Exception("The message is too long to encode in this image")
        _, stego_img = self.lsbCoding(img, message_in_binary)
        return stego_img


    def decodeMessage(self, path, password):
        mess = convertToString(self.lsbDecoding(path), password)        
        return mess


if __name__ == '__main__':
    lsb = Lsb()
    message = 'Hello World!'
    password = 'Haslo123'
    path = "path_to_image"
    stego_path = "path_to_stego_image"
    stego_img = lsb.codeMessage(path, message, password)
    stego_img.save(stego_path)

    print(lsb.decodeMessage(stego_path, password))


