from alg_des import adding_bits, permute, shift_left, hex2bin, ascii2bin, initial_perm, xor, bin2dec, dec2bin, dec2bin
from alg_des import final_perm, per, bin2ascii, keyp, key_comp,  exp_d, sbox, shift_table


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
        pt1_list = list(pt1)
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
