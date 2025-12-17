# backend# HideAndSeek 🕵️‍♂️🖼️



**HideAndSeek** to nowoczesna aplikacja webowa służąca do steganografii – sztuki ukrywania informacji. Aplikacja pozwala bezpiecznie ukrywać tajne wiadomości tekstowe wewnątrz plików graficznych PNG, wykorzystując zaawansowane metody manipulacji bitami oraz silne szyfrowanie.



## 🚀 Możliwości



* **Ukrywanie wiadomości (Encoding):** Zapisz sekretny tekst w obrazie PNG tak, aby był niewidoczny dla ludzkiego oka.

* **Odczytywanie wiadomości (Decoding):** Wydobądź ukrytą treść z obrazu, jeśli znasz hasło.

* **Szyfrowanie:** Każda wiadomość jest szyfrowana (AES/Fernet) przed ukryciem w obrazie. Bez hasła wiadomość jest niemożliwa do odczytania, nawet jeśli ktoś wyodrębni bity.

* **3 Metody Steganograficzne:** Wybierz algorytm najlepiej dopasowany do Twoich potrzeb (LSB, Huffman, Random LSB).

* **Nowoczesny Interfejs:** Ciemny motyw (Dark Mode), responsywny design i intuicyjna obsługa.



## 🛠️ Technologie



Projekt został zbudowany przy użyciu:

* **Backend:** Python 3, Flask

* **Przetwarzanie obrazu:** Pillow (PIL), NumPy

* **Kryptografia:** Biblioteka `cryptography` (Fernet/PBKDF2HMAC)

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)



## 🧠 Zastosowane Algorytmy



Aplikacja oferuje trzy metody ukrywania danych:



1.  **LSB (Least Significant Bit):**

    * Klasyczna metoda zastępująca ostatni bit każdego piksela bitem wiadomości.

    * Wiadomość jest zapisywana sekwencyjnie.



2.  **Random LSB:**

    * Bardziej dyskretna metoda. Oblicza "krok" (odstęp) na podstawie wielkości obrazka i długości wiadomości.

    * Rozprasza bity wiadomości po całym obrazie, zamiast skupiać je na początku pliku.



3.  **Huffman Coding:**

    * Kompresuje wiadomość przed ukryciem, używając kodowania Huffmana.

    * Pozwala ukryć więcej tekstu przy mniejszej ingerencji w obraz (zmienia mniej pikseli).

    * Zapisuje strukturę drzewa Huffmana w nagłówku obrazu.



## ⚙️ Instalacja i Uruchomienie



Aby uruchomić projekt lokalnie, postępuj zgodnie z poniższymi krokami:



### Wymagania

* Python 3.8+

* pip



### Kroki



1.  **Sklonuj repozytorium:**

    ```bash

    git clone https://github.com/MPZC/hideandseek

    cd HideAndSeek

    ```



2.  **Zalecane: Utwórz wirtualne środowisko:**

    ```bash

    python -m venv venv

    # Windows:

    venv\Scripts\activate

    # macOS/Linux:

    source venv/bin/activate

    ```



3.  **Zainstaluj zależności:**

    ```bash

    pip install -r requirements.txt

    ```



4.  **Uruchom aplikację:**

    ```bash

    python app.py

    ```



5.  **Otwórz w przeglądarce:**

    Wejdź na adres: `http://localhost:8080`



## 📖 Instrukcja Obsługi



### Kodowanie (Ukrywanie)

1.  Upewnij się, że przełącznik trybu jest ustawiony na **Encode**.

2.  Wybierz plik obrazu (format `.png`, maks. 5MB).

3.  Wybierz metodę kodowania (np. LSB).

4.  Wpisz tajną wiadomość.

5.  Ustaw silne hasło (Passphrase).

6.  Kliknij **Encode**. Po sukcesie pobierz wygenerowany obraz (`stego_image.png`).



### Dekodowanie (Odczytywanie)

1.  Przełącz tryb na **Decode** (suwak w górnym menu).

2.  Wgraj obraz zawierający ukrytą treść.

3.  Wybierz tę samą metodę, której użyto do zakodowania.

4.  Podaj hasło użyte przy kodowaniu.

5.  Kliknij **Decode**. Jeśli dane są poprawne, wiadomość pojawi się na ekranie.