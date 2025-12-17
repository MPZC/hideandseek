"""
Ten skrypt implementuje metodę ukrywania wiadomości w obrazach za pomocą zmodyfikowanego algorytmu LSB (Least Significant Bit).
Wiadomość jest zakodowana w najmniej znaczących bitach obrazu. Aby zakodować wiadomość, najpierw konwertuje się ją do postaci
binarnych ciągów, a następnie wstawia do wybranych pikseli obrazu, na podstawie obliczonego kroku. Odkodowanie działa na podobnej zasadzie
odczytując bity ukrytej wiadomości z najmniej znaczących bitów pikseli.

Moduły:
- `convertImage`  Konwertuje obraz na macierz numpy w celu ułatwienia manipulacji.
- `calculateStep`  Oblicza krok, co ile pikseli będzie zakodowany bit wiadomości.
- `lsbCoding`  Koduje wiadomość w obrazie, zmieniając ostatnie bity wybranych pikseli.
- `lsbDecoding`  Odkodowuje wiadomość z obrazu, odczytując najmniej znaczące bity pikseli.
- `codeExampleMessage`  Przykład zakodowania wiadomości w obrazie.
"""

import numpy as np
from PIL import Image
from .mess_preparation import *
from exceptions import *

class RandomLsb:
    # Konwertuje obraz na macierz numpy w celu manipulacji pikselami
    def convertImage(self, path):
        img = Image.open(path)
        numpy_img = np.array(img)
        return img, numpy_img


    '''Oblicza krok co ile pikseli zostaną zakodowane bity wiadomości.
    Jeśli wiadomość jest za długa dla danego obrazu, zwraca błąd.
    Zwraca:
    - Obliczony krok.
    '''
    def calculateStep(self, message_size, img):
        available = img.size - 11
        if (message_size) > available:
            max_chars = available // 7  # bo 7 bitów = 1 znak
            raise MessageTooLarge(
                f"Message is too long for this photo!\n"
                f"Max message length are: {max_chars} chars ({available} bits), "
                f"And you try to encode {message_size // 7} chars ({message_size} bits)."
            )
        
        step = max(1, available // message_size)

        if step > 1023:
            raise MessageTooShort(
                f"The message is too short. The step is {step}, "
                "the max step is 1024.\n"
                "Try to use longer message or smaller picture."
            )

        return step


    '''Koduje wiadomość w obrazie poprzez zmianę najmniej znaczących bitów wybranych pikseli.
    Zwraca:
    1. Obraz zakodowany w formacie numpy
    2. Obraz zakodowany w formacie PIL (do zapisu)
    '''
    def rlsbCoding(self, img, message, step):
        shape = img.shape     # Kształt obrazu do przywrócenia po modyfikacji
        size = img.size
        resized_img = img.reshape(1, size)  # Zmiena obrazu na tablicę jednowymiarową
        pixel = 0              # Zmienna kontrolująca przemieszczanie się po pikselach 
        # Kodowanie nagłówka
        for bit in range(0, 10):
            if message[bit] == '0':
                resized_img[0, pixel] = resized_img[0, pixel] & ~1  # Wyzerowanie ostatniego bitu
            elif message[bit] == '1':
                resized_img[0, pixel] = resized_img[0, pixel] | 1   # Ustawia ostatni bit na 1
            else:
                print("Błąd")
            pixel += 1
        
        pixel += 1
        # Kodowanie wiadomości
        for bit in range(10, len(message)):
            if message[bit] == '0':
                resized_img[0, pixel] = resized_img[0, pixel] & ~1  # Wyzerowanie ostatniego bitu
            elif message[bit] == '1':
                resized_img[0, pixel] = resized_img[0, pixel] | 1   # Ustawia ostatni bit na 1
            else:
                print("Błąd")
            pixel += step

        new_img = resized_img.reshape(shape)  # Przywrócenie pierwotnego kształtu obrazu
        pil_image = Image.fromarray(new_img)  # Tworzenie obrazu w formacie PIL
        return new_img, pil_image


    # Odkodowuje wiadomość z obrazu, czytając najmniej znaczące bity pikseli
    def rlsbDecoding(self, img_path):
        _, img = self.convertImage(img_path)
        message = ''
        resized_img = img.reshape(1, img.size)
        step = ''
        size_of_text = ''

        # Read step (10 pierwszych bitów)
        for bit in range(0, 10):
            if resized_img[0, bit] % 2 == 0:
                step += '0'
            elif resized_img[0, bit] % 2 == 1:
                step += '1'
            else:
                print("Błąd")
        step = int(step, 2) # Zmiana z postaci binarnej
            
        # Odczytanie długości wiadomości
        for bit in range(11, (20*step)+11, step):
            if resized_img[0, bit] % 2 == 0:
                size_of_text += '0'
            elif resized_img[0, bit] % 2 == 1:
                size_of_text += '1'
            else:
                print("Błąd")
        size_of_text = int(size_of_text, 2) + 20

        # Odczytanie wiadomości (od miejsca w którym zakończyliśmy czytać długość wiadomości)
        for bit in range((20*step)+11, (size_of_text*step)+11, step):
            if resized_img[0, bit] % 2 == 0:
                message += '0'
            elif resized_img[0, bit] % 2 == 1:
                message += '1'
            else:
                print("Błąd")
        return message 


    def codeMessage(self, path, message, password):
        _, img = self.convertImage(path)
        temp_binary = convertToBinary(message, password)  # Message without step
        cal_step = self.calculateStep(len(temp_binary), img) # Calculate step with number od bites
        message_in_binary= convertToBinary(message, password, cal_step)
        _, stego_img = self.rlsbCoding(img, message_in_binary, cal_step)
        return stego_img


    def decodeMessage(self, path, password):
        mess = convertToString(self.rlsbDecoding(path), password)
        print(f"Message: {mess}")
        return mess[2:]


if __name__ == '__main__':
    message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum dignissim urna eget egestas porta. Aenean eget eros dapibus, fringilla nisi vel, tincidunt ex. Integer vitae vulputate nisi. Cras egestas sem lorem, vel maximus metus ultricies ac. Praesent lobortis egestas dignissim. Etiam porttitor faucibus erat. Curabitur dapibus sem at faucibus facilisis."
    message2 = "Hello World!"
    password = 'Haslo123'
    path = 'path_to_image'
    stegano_path = 'path_to_stego_image'

    rlsb = RandomLsb()
    stego_img = rlsb.codeMessage(path, message2, password)
    stego_img.save(stegano_path)
    rlsb.decodeMessage(stegano_path, password)


