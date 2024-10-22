from calendar import different_locale
from alg_des import shift_table, adding_bits, permute, shift_left, hex2bin, key_comp
from alg_des import keyp, ascii2bin, exp_d, initial_perm, xor, bin2dec, sbox, dec2bin, dec2bin
from alg_des import final_perm, per, bin2ascii


def get_rkb(pt, key, encoding):
    key = adding_bits(key)
	# getting 56 bit key from 64 bit using the parity bits
    key = permute(key, keyp, 56)
    c = key[:28] # rkb for RoundKeys in binary
    d = key[28:] # rk for RoundKeys in hexadecimal

    rkb = []
    for i in range(16):
	    # Shifting the bits by nth shifts by checking from shift table
        c = shift_left(c, shift_table[i])
        d = shift_left(d, shift_table[i])
        combine_str = c + d
        # Compression of key from 56 to 48 bits
        round_key = permute(combine_str, key_comp, 48)
        rkb.append(round_key)
    return rkb

def encrypt_rk(pt, rkb, n):
    # Initial Permutation
    pt = permute(pt, initial_perm, 64)

    # Splitting
    left = pt[:32]
    right = pt[32:]
	# Expansion D-box: Expanding the 32 bits data into 48 bits
    right_expanded = permute(right, exp_d, 48)
    # XOR RoundKey[i] and right_expanded
    xor_x = xor(right_expanded, rkb[n])
    # S-boxex: substituting the value from s-box table by calculating row and column
    sbox_str = ""
    for j in range(8):
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
    if n != 15:
        left, right = right, left
    combine = left + right
    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text


def calculate_avalanche(pt, key, encoding, bit_position):
    if encoding == 'hex':
        pt1 = hex2bin(pt)
        pt1_list = list(pt1)
        key = hex2bin(key)
    else:
        pt1 = ascii2bin(pt)
        key = ascii2bin(key)
    if pt1_list[bit_position] == '1':
        pt1_list[bit_position] = '0'
    else:
        pt1_list[bit_position] = '1'
    pt2_list = pt1_list
    pt2 = ''.join(pt2_list)

    rkb1 = get_rkb(pt1, key, encoding)
    rkb2 = get_rkb(pt2, key, encoding)

    differents_pt = []
    for i in range(16):
        ct1 = encrypt_rk(pt1, rkb1, i)
        ct2 = encrypt_rk(pt2, rkb2, i)
        differents_pt.append(sum(c1 != c2 for c1, c2 in zip(ct1, ct2)))


    key1 = key
    key1_list = list(key)
    if key1_list[bit_position] == '1':
        key1_list[bit_position] = '0'
    else:
        key1_list[bit_position] = '1'
    key2_list = key1_list
    key2 = ''.join(key2_list)
    differents_key = []

    rkb1 = get_rkb(pt1, key1, encoding)
    rkb2 = get_rkb(pt1, key2, encoding)

    for i in range(16):
        ct1 = encrypt_rk(pt1, rkb1, i)
        ct2 = encrypt_rk(pt2, rkb2, i)
        differents_key.append(sum(c1 != c2 for c1, c2 in zip(ct1, ct2)))

    return differents_pt, differents_key


































'''

# Функция для изменения заданного бита
def flip_bit(data, bit_position):
    """Меняет бит в заданной позиции."""
    bit_list = list(data)
    bit_list[bit_position] = '0' if bit_list[bit_position] == '1' else '1'
    return ''.join(bit_list)

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

'''