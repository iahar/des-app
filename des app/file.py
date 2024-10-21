import binascii
import time
# -*- coding: utf-8 -*-

def process_key(key_input):
    # Преобразование ключа в байты
    return key_input.encode('utf-8')

def encrypt_decrypt(text, key):
    # Преобразование текста и ключа в байты
    text_bytes = text.encode('utf-8')
    key_bytes = key * (len(text_bytes) // len(key) + 1)

    # Применение XOR для каждого байта
    result_bytes = bytes([b ^ k for b, k in zip(text_bytes, key_bytes)])

    # Возврат зашифрованного текста как строки
    return result_bytes

def decrypt(encrypted_bytes, key):
    # Дешифрование аналогично шифрованию, просто применяем XOR снова
    key_bytes = key * (len(encrypted_bytes) // len(key) + 1)
    result_bytes = bytes([b ^ k for b, k in zip(encrypted_bytes, key_bytes)])
    return result_bytes.decode('utf-8')

def to_hex(text):
    return binascii.hexlify(text).decode()

def from_hex(hex_text):
    return binascii.unhexlify(hex_text)

def save_file_hex(text, default_filename):
    # Запрос имени файла у пользователя
    filename = input(f"Введите имя файла для сохранения (нажмите Enter для использования имени '{default_filename}'): ")

    # Если пользователь не ввёл имя файла, используем имя по умолчанию
    if filename == '':
        filename = default_filename

    # Сохраняем текст в шестнадцатеричном виде
    with open(filename, 'w') as f:
        f.write(binascii.hexlify(text).decode())
    print(f"Текст сохранен в файл: {filename} (в шестнадцатеричном виде)")

def read_file_hex(filename):
    # Чтение текста в шестнадцатеричном формате и преобразование его обратно
    with open(filename, 'r') as f:
        hex_content = f.read()
    return binascii.unhexlify(hex_content)

def view_and_edit_data(data, data_type, is_encrypted=False):
    # Отображение данных в символьном виде (если это не зашифрованный текст)
    if not is_encrypted:
        print(f"{data_type} в символьном виде: {data.decode('utf-8')}")

    # Отображение данных в шестнадцатеричном виде
    hex_data = to_hex(data)
    print(f"{data_type} в шестнадцатеричном виде: {hex_data}")

    # Возможность изменения
    choice = input(f"Хотите изменить {data_type}? (y/n): ").lower()
    if choice == 'y':
        format_choice = input("Вы хотите изменить данные в символьном (1) или шестнадцатеричном (2) виде? ")
        if format_choice == '1' and not is_encrypted:
            data = input(f"Введите новый {data_type} в символьном виде: ").encode('utf-8')
        elif format_choice == '2':
            hex_data = input(f"Введите новый {data_type} в шестнадцатеричном виде: ")
            data = from_hex(hex_data)

    return data

def main():
    print("Выберите процедуру:\n1. Зашифровать открытый текст\n2. Расшифровать текст\n")
    menu_action = int(input())

    if menu_action == 1:
        key_input = input("Введите 16-буквенный ключ: ")
        if len(key_input) != 16:
            print("Ошибка: ключ должен быть длиной 16 символов.")
            return

        key = process_key(key_input)
        text = input("Введите текст для шифрования: ")

        # Шифрование
        encrypted_text = encrypt_decrypt(text, key)

        # Сохранение зашифрованного текста в шестнадцатеричном виде
        save_file_hex(encrypted_text, 'encrypted.txt')

    elif menu_action == 2:
        key_input = input("Введите 16-буквенный ключ: ")
        if len(key_input) != 16:
            print("Ошибка: ключ должен быть длиной 16 символов.")
            return

        key = process_key(key_input)

        # Чтение зашифрованного текста в шестнадцатеричном формате
        filename = input("Введите имя файла с зашифрованным текстом: ")
        encrypted_text = read_file_hex(filename)

        # Расшифрование
        decrypted_text = decrypt(encrypted_text, key)

        # Сохранение расшифрованного текста
        save_file_hex(decrypted_text.encode('utf-8'), 'decrypted.txt')

    else:
        print('Неверный параметр. Выберите 1 или 2.')
        return


