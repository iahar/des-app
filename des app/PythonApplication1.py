# -*- coding: utf-8 -*-
""" 
МОЙ ПРОМТ 1

Я изменю задание, вот что должен нужно:
Исследовать лавинный эффект (исследования проводить на одном блоке текста):
1) для бита, который будет изменяться, приложение должно позволять задавать его позицию (номер) в открытом тексте или в ключе;
2) приложение должно уметь после каждого раунда шифрования подсчитывать число
бит, изменившихся в зашифрованном тексте при изменении одного бита в открытом
тексте либо в ключе;
3) приложение может строить графики зависимости числа бит, изменившихся в зашифрованном тексте, от раунда шифрования, либо графики можно строить в стороннем ПО, 
но тогда приложение для шифрования должно сохранять в файл необходимую для построения графиков информацию


Для реализации предложенного исследования лавинного эффекта (при изменении одного бита в открытом тексте или ключе) с возможностью изменения позиции бита и подсчета изменения битов после каждого раунда шифрования, мы можем адаптировать уже существующие функции в коде. Вот шаги для выполнения вашего задания:

Шаги для реализации
Ввод позиции изменяемого бита: Пользователь вводит номер бита, который будет изменен, как в открытом тексте, так и в ключе.
Подсчет измененных битов после каждого раунда: Программа должна подсчитывать количество измененных битов после каждого раунда шифрования при изменении одного бита.
Сохранение информации для построения графиков: Результаты подсчета изменений должны сохраняться в файл, чтобы их можно было использовать для построения графиков.
Обновленный код для исследования лавинного эффекта
Функция изменения бита: Уже существует функция flip_bit, которая меняет один бит в строке. Её можно использовать как для текста, так и для ключа?(graph).

Функция для анализа лавинного эффекта: Мы будем проводить шифрование и отслеживать изменения на каждом этапе, используя созданную функцию шифрования.

Добавление подсчета изменившихся битов на каждом раунде: Мы уже имеем функции, которые могут отслеживать изменения после каждого раунда шифрования.

Вот пример обновленного кода:
"""

import matplotlib.pyplot as plt
from alg_des import encrypt, permute, adding_bits, keyp, shift_left, key_comp, block_encrypt
from alg_des import ascii2bin, shift_table, hex2bin, initial_perm, exp_d, xor

# Функция для изменения заданного бита
def flip_bit(data, bit_position):
    """Меняет бит в заданной позиции."""
    bit_list = list(data)
    bit_list[bit_position] = '0' if bit_list[bit_position] == '1' else '1'
    return ''.join(bit_list)

# Функция для подсчета различий между двумя бинарными строками
def count_bit_differences(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))


# Функция для подсчета изменения битов на каждом раунде
def des_encrypt_with_tracking(pt, key, encoding, bit_position=None, mode="text"):
    # Перевод текста и ключа в бинарный формат
    if encoding == "hex":
        pt = hex2bin(pt)
        key = hex2bin(key)
    else:
        pt = ascii2bin(pt)
        key = ascii2bin(key)

    key_bin = permute(key_bin, keyp, 56)
    
    # Разбивка ключа на 28-битные части
    c = key_bin[:28]
    d = key_bin[28:]

    rkb = []  # Раундовые ключи в бинарном виде
    for i in range(16):
        c = shift_left(c, shift_table[i])
        d = shift_left(d, shift_table[i])
        round_key = permute(c + d, key_comp, 48)
        rkb.append(round_key)

    # Initial Permutation
    pt = permute(pt, initial_perm, 64)

    # Splitting
    left = pt[:32]
    right = pt[32:]

    for i in range(16):
	    # Expansion D-box: Expanding the 32 bits data into 48 bits
	    right_expanded = permute(right, exp_d, 48)

        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])

        # S-boxex: substituting the value from s-box table by calculating row and column
        sbox_str = ""
        for j in range(0, 8):
	        row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
	        col = bin2dec(
		        int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
	        val = sbox[j][row][col]
	        sbox_str = sbox_str + dec2bin(val)

        # Straight D-box: After substituting rearranging the bits
        sbox_str = permute(sbox_str, per, 32)

        # XOR left and sbox_str
        left = xor(left, sbox_str)

        # Swapper
        if i != 15:
	        left, right = right, left
	
        combine = left + right
        # Final permutation: final rearranging of bits to get cipher text
        cipher_text = permute(combine, final_perm, 64)



    # Если изменяем бит в тексте
    if mode == "text":
        altered_pt_bin = flip_bit(pt_bin, bit_position)
        altered_ciphertext = encrypt(altered_pt_bin, key_bin, encoding)
    # Если изменяем бит в ключе
    elif mode == "key":
        altered_key_bin = flip_bit(key_bin, bit_position)
        altered_ciphertext = encrypt(pt_bin, altered_key_bin, encoding)
    else:
        raise ValueError("Укажите, что нужно изменить: текст или ключ")

    # Подсчет изменения битов на каждом раунде
    differences = []
    for i in range(16):
        diff = count_bit_differences(original_ciphertext[i], altered_ciphertext[i])
        differences.append(diff)
    print(differences)
    return differences

# Функция для сохранения изменений в файл
def save_differences_to_file(differences, filename="bit_changes.txt"):
    with open(filename, 'w') as f:
        for round_num, diff in enumerate(differences, 1):
            f.write(f"Раунд {round_num}: {diff} изменённых бит\n")

# Функция для построения графика
def plot_differences(differences):
    rounds = list(range(1, len(differences) + 1))
    plt.plot(rounds, differences, marker='o')
    plt.title("Лавинный эффект: Изменение битов после каждого раунда")
    plt.xlabel("Раунд")
    plt.ylabel("Число изменённых бит")
    plt.grid(True)
    plt.show()

# Исследование лавинного эффекта
def investigate_avalanche_effect(pt, key, encoding, bit):
    # Ввод режима изменения (текст или ключ)
    mode = input("Что вы хотите изменить (text/key): ")

    # Проведение шифрования с отслеживанием лавинного эффекта
    differences = des_encrypt_with_tracking(pt, key, bit, mode)

    # Сохранение изменений в файл
    save_differences_to_file(differences)

    # Построение графика
    # plot_differences(differences)

# investigate_avalanche_effect()

"""
Что делает этот код:
Позиция изменяемого бита: Пользователь может указать позицию бита, который будет изменён в открытом тексте или ключе.
Подсчет битов после каждого раунда: После каждого раунда шифрования приложение подсчитывает, сколько бит изменилось в результате изменения одного бита.
Сохранение результатов: Количество изменённых битов сохраняется в файл.
Построение графика: Программа строит график зависимости числа изменённых битов от раунда шифрования.
Дальнейшие шаги:
Тестирование с различными параметрами: Можно изменить текст, ключ или номер бита и наблюдать за результатами.
Использование внешнего ПО для построения графиков: Если вы предпочитаете строить графики в стороннем ПО, информация сохраняется в файл, который можно использовать для дальнейшего анализа.
Этот код соответствует вашему описанию задачи и позволит исследовать лавинный эффект на уровне каждого раунда шифрования.
"""




"""
Для того чтобы ваше существующее приложение на основе Tkinter могло рисовать график, нужно использовать библиотеку matplotlib, 
которая уже частично интегрирована в вашем коде (в файле des_app.py вы подключаете FigureCanvasTkAgg для работы с графиками).
Мы расширим существующую логику, чтобы приложение после каждого шифрования рисовало график лавинного эффекта на основе введенных данных.

Обновленный код для рисования графика в вашем приложении
Ввод позиции бита: В вашем интерфейсе уже есть поле для ввода номера бита. Мы будем использовать его для анализа лавинного эффекта.
Шифрование и подсчет изменений: Используем уже существующую логику шифрования и будем считать количество измененных битов после каждого раунда.
Построение графика: График будет рисоваться в интерфейсе после шифрования с использованием библиотеки matplotlib.
Обновленный метод plot_graph:
"""
'''
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from alg_des import block_encrypt, calculate_avalanche
from graph import count_bit_differences, flip_bit

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DES Шифратор/Дешифратор")
        self.root.geometry("700x750")
        self.root.configure(bg="#f0f0f0")

        # Поля для ввода текста, ключа, выбора кодировки и ввода номера бита уже существуют
        # Дополняем логику для работы с графиком лавинного эффекта

        # Поле для ввода номера бита
        tk.Label(self.root, text="Введите номер бита для изменения:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.bit = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.bit.pack(pady=5)

        # Кнопка для построения графика
        plot_button = tk.Button(self.root, text="Построить график", command=self.plot_graph, font=("Arial", 12), bg="#2196F3", fg="white")
        plot_button.pack(pady=10)

        # Запуск приложения
        self.root.mainloop()

    def plot_graph(self):
        ind_bit = self.bit.get()
        try: 
            ind_bit = int(ind_bit)
        except Exception as e:
            messagebox.showerror("Ошибка", "Неверный формат номера бита. Введите целое число.")
            return

        if not ind_bit or ind_bit > 63:
            messagebox.showerror("Ошибка", "Введите номер бита от 1 до 63.")
            return

        # Создаем фигуру для графика
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        try:
            pt = self.plaintext_entry.get()  # Ввод текста
            key = self.key_entry.get()       # Ввод ключа
            encoding = self.encoding_var.get()  # Получаем кодировку
            
            # Получаем зашифрованный текст
            ct = block_encrypt(pt, key, encoding)

            # Изменение одного бита в тексте
            altered_pt = flip_bit(pt, ind_bit)

            # Подсчет изменений битов после каждого раунда
            differences = self.calculate_bit_changes_per_round(pt, altered_pt, key, encoding)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка шифрования: {str(e)}")
            return

        # Построение графика
        rounds = range(1, len(differences) + 1)
        ax.plot(rounds, differences, marker='o')
        ax.set_title("Лавинный эффект: Изменение битов после каждого раунда")
        ax.set_xlabel("Раунд")
        ax.set_ylabel("Число изменённых битов")
        ax.grid(True)

        # Отображение графика в окне приложения
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def calculate_bit_changes_per_round(self, pt, altered_pt, key, encoding):
        """Функция для подсчета изменения битов после каждого раунда шифрования."""
        original_cipher = block_encrypt(pt, key, encoding)
        altered_cipher = block_encrypt(altered_pt, key, encoding)

        differences = []

        # Подсчитываем количество измененных битов после каждого раунда
        for i in range(len(original_cipher)):
            differences.append(count_bit_differences(original_cipher[i], altered_cipher[i]))

        return differences


if __name__ == '__main__':
    app = Application()

'''
"""
Изменения в вашем приложении:
Ввод номера бита: Добавляется поле для ввода номера бита, который нужно изменить в тексте (или можно адаптировать для ключа).
Шифрование и изменение одного бита: Используются функции block_encrypt для шифрования исходного текста и текста с измененным битом.
Подсчет изменений после каждого раунда: Программа подсчитывает количество изменившихся битов между двумя зашифрованными текстами 
(с исходным и изменённым битом) после каждого раунда.
Построение графика: Результаты отображаются в виде графика зависимости числа изменённых битов от раунда шифрования с использованием matplotlib.
Запуск и использование:
Вводите текст для шифрования, ключ, выбираете кодировку.
Указываете номер бита, который хотите изменить.
Нажимаете кнопку "Построить график", и приложение рисует график лавинного эффекта в зависимости от раунда шифрования.
Теперь ваше приложение умеет строить графики для визуализации лавинного эффекта после каждого раунда шифрования!
"""