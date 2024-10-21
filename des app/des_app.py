# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, StringVar
from alg_des import encrypt, decrypt
from alg_app import main

class Application:
    def __init__(self):
        # Создание главного окна
        self.root = tk.Tk()
        self.root.title("DES Шифратор/Дешифратор")
        self.root.geometry("700x500")  # Установка размера окна
        self.root.configure(bg="#f0f0f0")  # Установка фона окна

        # Заголовок
        title_label = tk.Label(self.root, text="DES Шифратор/Дешифратор", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Ввод текста для шифрования
        tk.Label(self.root, text="Введите текст для шифрования:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.plaintext_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.plaintext_entry.pack(pady=5)

        # Ввод ключа
        tk.Label(self.root, text="Введите 7-символьный ключ:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.key_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.key_entry.pack(pady=5)

        # Выбор кодировки
        tk.Label(self.root, text="Выберите кодировку:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.encoding_var = StringVar(self.root)
        self.encoding_var.set("hex")  # Установка значения по умолчанию
        encoding_options = ["hex", "ascii"]
        encoding_menu = tk.OptionMenu(self.root, self.encoding_var, *encoding_options)
        encoding_menu.config(font=("Arial", 12))
        encoding_menu.pack(pady=5)

        # Кнопка шифрования
        encrypt_button = tk.Button(self.root, text="Зашифровать", command=self.encrypt_text, font=("Arial", 12), bg="#4CAF50", fg="white")
        encrypt_button.pack(pady=10)

        # Ввод текста для расшифрования
        tk.Label(self.root, text="Введите текст для расшифрования:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.ciphertext_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.ciphertext_entry.pack(pady=5)

        # Кнопка расшифрования
        decrypt_button = tk.Button(self.root, text="Расшифровать", command=self.decrypt_text, font=("Arial", 12), bg="#f03987", fg="white")
        decrypt_button.pack(pady=10)

        # Метка для отображения результата
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f0f0")
        self.result_label.pack(pady=20)

        # Запуск приложения
        self.root.mainloop()

    def encrypt_text(self):
        plaintext = self.plaintext_entry.get()
        key = self.key_entry.get()
        encoding = self.encoding_var.get()  # Получаем выбранную кодировку

        if not key or len(key) != 7:  # Убедитесь, что ключ 7 символов
            messagebox.showerror("Ошибка", "Ключ должен содержать 7 символов.")
            return

        # Применяем кодировку
        try:
            plaintext_encoded = plaintext.encode(encoding)
            ciphertext = encrypt(plaintext_encoded, key)
            self.result_label.config(text=f"Зашифрованный текст: {ciphertext}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка кодировки: {str(e)}")

    def decrypt_text(self):
        ciphertext = self.ciphertext_entry.get()
        key = self.key_entry.get()
        encoding = self.encoding_var.get()  # Получаем выбранную кодировку

        if not key or len(key) != 7:  # Убедитесь, что ключ 7 символов
            messagebox.showerror("Ошибка", "Ключ должен содержать 7 символов.")
            return

        # Применяем кодировку
        try:
            plaintext = decrypt(ciphertext, key)
            plaintext_decoded = plaintext.decode(encoding)
            self.result_label.config(text=f"Расшифрованный текст: {plaintext_decoded}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка кодировки: {str(e)}")

    @staticmethod
    def keypress(event):
        if event.keycode == 86:
            event.widget.event_generate('<<Paste>>')
        elif event.keycode == 67:
            event.widget.event_generate('<<Copy>>')
        elif event.keycode == 88:
            event.widget.event_generate('<<Cut>>')


if __name__ == '__main__':
    #app = Application()
    main()


