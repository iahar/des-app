import matplotlib.pyplot as plt


# Функция для изменения заданного бита
def flip_bit(data, bit_position):
    """Меняет бит в заданной позиции."""
    bit_list = list(data)
    bit_list[bit_position] = '0' if bit_list[bit_position] == '1' else '1'
    return ''.join(bit_list)

# Функция для подсчета различий между двумя бинарными строками
def count_bit_differences(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))
# Функция для изменения заданного бита
def flip_bit(data, bit_position):
    """Меняет бит в заданной позиции."""
    bit_list = list(data)
    bit_list[bit_position] = '0' if bit_list[bit_position] == '1' else '1'
    return ''.join(bit_list)

# Функция для подсчета различий между двумя бинарными строками
def count_bit_differences(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

# Функция для записи данных в файл для построения графика
def save_differences_to_file(differences, filename):
    with open(filename, 'w') as file:
        for round_num, diff in enumerate(differences, 1):
            file.write(f"Раунд {round_num}: {diff} бит изменено\n")

# Функция для отображения графика
def plot_differences(differences):
    rounds = list(range(1, len(differences) + 1))
    plt.plot(rounds, differences, marker='o')
    plt.title("Лавинный эффект: Изменение битов после каждого раунда")
    plt.xlabel("Раунд")
    plt.ylabel("Число изменённых бит")
    plt.grid(True)
    plt.show()
def des_encrypt_with_tracking(pt, key, altered_pt=None, altered_key=None, mode="text"):
    key = ascii2bin(key)
    pt = ascii2bin(pt)
    key = adding_bits(key)
    key = permute(key, keyp, 56)
    c = key[:28]
    d = key[28:]

    rkb = []
    rk = []

    for i in range(16):
        c = shift_left(c, shift_table[i])
        d = shift_left(d, shift_table[i])
        round_key = permute(c + d, key_comp, 48)
        rkb.append(round_key)
        rk.append(bin2ascii(round_key))

    original_pt = pt
    original_cipher = encrypt(pt, key)

    if mode == "text" and altered_pt:
        altered_pt = ascii2bin(altered_pt)
        altered_cipher = encrypt(altered_pt, key)
    elif mode == "key" and altered_key:
        altered_key = ascii2bin(altered_key)
        altered_cipher = encrypt(pt, altered_key)
    else:
        raise ValueError("Не указан изменённый текст или ключ")

    differences = []

    for i in range(16):
        original_cipher_bits = permute(original_cipher, final_perm, 64)
        altered_cipher_bits = permute(altered_cipher, final_perm, 64)
        difference = count_bit_differences(original_cipher_bits, altered_cipher_bits)
        differences.append(difference)

    return differences

# Функция для исследования лавинного эффекта
def investigate_avalanche_effect():
    pt = "example_text"
    key = "secret_k"

    altered_pt = flip_bit(ascii2bin(pt), 10)

    differences = des_encrypt_with_tracking(pt, key, altered_pt=altered_pt, mode="text")

    save_differences_to_file(differences, "bit_changes.txt")
    plot_differences(differences)
investigate_avalanche_effect()