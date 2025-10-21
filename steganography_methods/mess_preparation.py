
def convertToBinary(message, step=None):
    print(f"Kodowanie wiadomości: {message}")
    message = "**" + message
    table_of_bin = []
    len_of_message = (len(message)*7)
    print(len_of_message)
    len_of_message_bin = bin(len_of_message)[2:].zfill(20)
    message_in_binary = len_of_message_bin
    if step:
        if step>1023:
            raise Exception("Zbyt krótka wiadomość")
        step_bin = bin(step)[2:].zfill(10)
        message_in_binary = step_bin + len_of_message_bin

    # Konwersja każdego znaku do formatu binarnego
    for char in message:
        bin_repr = bin(ord(char))[2:].zfill(7)
        table_of_bin.append(bin_repr)

    for b in table_of_bin:
        message_in_binary += b

    return message_in_binary


def convertToString(message_in_binary):
    print(f"Message in binary: {message_in_binary}")
    table_of_strings = []
    message = ""
    for char in range(0, len(message_in_binary), 7):
        table_of_strings.append(chr(int(message_in_binary[char:char+7], 2)))

    for i in table_of_strings:
        message += i

    return message

