# -*- coding: utf-8 -*-
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox, StringVar
import os
from alg_des import block_encrypt, block_decrypt
from graph import calculate_avalanche
from criteria import calculate


class Application:
    def __init__(self):
        # Инициализация главного окна
        self.root = tk.Tk()
        self.root.title("DES Шифратор/Дешифратор")
        self.root.geometry("700x900")  # Установка размера окна
        self.root.configure(bg="#f0f0f0")  # Установка фона окна

        # Заголовок
        title_label = tk.Label(self.root, text="DES Шифратор/Дешифратор", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=5)

        # Ввод текста для шифрования
        tk.Label(self.root, text="Введите текст для шифрования:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.plaintext_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.plaintext_entry.pack(pady=5)

        # Ввод ключа
        tk.Label(self.root, text="Введите ключ 8-символьный (ascii) 16-символьный (hex):", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
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
        encrypt_button.pack(pady=5)

        # Ввод текста для расшифрования
        tk.Label(self.root, text="Введите текст для расшифрования:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.ciphertext_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.ciphertext_entry.pack(pady=5)

        # Кнопка расшифрования
        decrypt_button = tk.Button(self.root, text="Расшифровать", command=self.decrypt_text, font=("Arial", 12), bg="#f03987", fg="white")
        decrypt_button.pack(pady=5)

        # Метка для отображения результата
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        # Ввод номера бита
        tk.Label(self.root, text="Введите номер бита для изменения:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.bit = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.bit.pack(pady=5)

        # Кнопка для построения графика
        plot_button = tk.Button(self.root, text="Построить график", command=self.plot_graph, font=("Arial", 12), bg="#2196F3", fg="white")
        plot_button.pack(pady=10)

        # Загрузка данных из файлов при запуске
        self.load_data()

        # Запуск приложения
        self.root.mainloop()

    def save_data(self):
        """Сохраняем текст, ключ и кодировку в файлы."""
        try:
            # Сохраняем текст для шифрования
            with open("plaintext.txt", "w") as pt_file:
                pt_file.write(self.plaintext_entry.get())

            # Сохраняем ключ
            with open("key.txt", "w") as key_file:
                key_file.write(self.key_entry.get())

            # Сохраняем кодировку
            with open("encoding.txt", "w") as encoding_file:
                encoding_file.write(self.encoding_var.get())

            messagebox.showinfo("Успешно", "Данные успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def load_data(self):
        """Загружаем текст, ключ и кодировку из файлов (если они существуют)."""
        try:
            # Загружаем текст для шифрования
            if os.path.exists("plaintext.txt"):
                with open("plaintext.txt", "r") as pt_file:
                    self.plaintext_entry.insert(0, pt_file.read())

            # Загружаем ключ
            if os.path.exists("key.txt"):
                with open("key.txt", "r") as key_file:
                    self.key_entry.insert(0, key_file.read())

            # Загружаем кодировку
            if os.path.exists("encoding.txt"):
                with open("encoding.txt", "r") as encoding_file:
                    self.encoding_var.set(encoding_file.read())
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def save_encryption_result(self, ciphertext):
        """Сохраняем результат шифрования в файл."""
        try:
            with open("ciphertext.txt", "w") as ct_file:
                ct_file.write(ciphertext)
            messagebox.showinfo("Успешно", "Результат шифрования сохранен в файл.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить результат шифрования: {str(e)}")

    def encrypt_text(self):
        plaintext = self.plaintext_entry.get()
        key = self.key_entry.get()
        encoding = self.encoding_var.get()  # Получаем выбранную кодировку
        
        if not key:
            if encoding == 'ascii' and len(key) != 8:  # Убедитесь, что ключ 8 символов
                messagebox.showerror("Ошибка", "Ключ должен содержать 8 символов.")
                return
            elif encoding == 'hex' and len(key) != 14:
                messagebox.showerror("Ошибка", "Ключ должен содержать 14 символов.")
                return
            
        try:
            ciphertext = block_encrypt(plaintext, key, encoding)
            self.result_label.config(text=f"Зашифрованный текст: {ciphertext}")

            # Сохраняем результат шифрования в файл
            self.save_encryption_result(ciphertext)

            # Сохраняем данные (текст, ключ, кодировку)
            self.save_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка кодировки: {str(e)}")

    def decrypt_text(self):
        ciphertext = self.ciphertext_entry.get()
        key = self.key_entry.get()
        encoding = self.encoding_var.get()  # Получаем выбранную кодировку

        if not key:
            if encoding == 'ascii' and len(key) != 8:  # Убедитесь, что ключ 8 символов
                messagebox.showerror("Ошибка", "Ключ должен содержать 8 символов.")
                return
            elif encoding == 'hex' and len(key) != 14:
                messagebox.showerror("Ошибка", "Ключ должен содержать 14 символов.")
                return

        try:
            plaintext = block_decrypt(ciphertext, key, encoding)
            self.result_label.config(text=f"Расшифрованный текст: {plaintext}")
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

    def plot_graph(self):
        ind_bit = self.bit.get()
        try: 
            ind_bit = int(ind_bit)
        except Exception as e:
            return
        if not ind_bit or int(ind_bit) > 16:
            messagebox.showerror("Ошибка", "Введите номер бита от 1 до 16.")
            return

        # Удаляем предыдущий график, если он существует
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()

        # Создаем фигуру для графиков
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 8), dpi=100)  # Два подграфика

        # Создаем массив для графиков
        x = range(1, 17)        
        try:
            pt = self.plaintext_entry.get()
            key = self.key_entry.get()
            encoding = self.encoding_var.get() 
            y_pt, y_key = calculate_avalanche(pt, key, encoding, ind_bit-1)
        except Exception as e:
            messagebox.showerror("Нет данных для построения.", f"Ошибка: {str(e)}")
            return

        # Очищаем предыдущие графики
        ax1.clear()
        ax2.clear()

        # Построение первого графика
        ax1.plot(x, y_pt, label='Avalanche Effect - Plaintext', color='blue')
        ax1.set_xlabel('Раунд')
        ax1.set_ylabel('Значение')
        ax1.legend()
        ax1.grid()

        # Построение второго графика
        ax2.plot(x, y_key, label='Avalanche Effect - Key', color='red')
        ax2.set_xlabel('Раунд')
        ax2.set_ylabel('Значение')
        ax2.legend()
        ax2.grid()

        # Создаем canvas для отображения графиков
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == '__main__':
    app = Application()
    calculate()
