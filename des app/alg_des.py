from cgitb import enable
import time
import os

# Table of Position of 64 bits at initial level: Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
				60, 52, 44, 36, 28, 20, 12, 4,
				62, 54, 46, 38, 30, 22, 14, 6,
				64, 56, 48, 40, 32, 24, 16, 8,
				57, 49, 41, 33, 25, 17, 9, 1,
				59, 51, 43, 35, 27, 19, 11, 3,
				61, 53, 45, 37, 29, 21, 13, 5,
				63, 55, 47, 39, 31, 23, 15, 7]

# Expansion D-box Table
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
		6, 7, 8, 9, 8, 9, 10, 11,
		12, 13, 12, 13, 14, 15, 16, 17,
		16, 17, 18, 19, 20, 21, 20, 21,
		22, 23, 24, 25, 24, 25, 26, 27,
		28, 29, 28, 29, 30, 31, 32, 1]

# Straight Permutation Table
per = [16, 7, 20, 21,
	29, 12, 28, 17,
	1, 15, 23, 26,
	5, 18, 31, 10,
	2, 8, 24, 14,
	32, 27, 3, 9,
	19, 13, 30, 6,
	22, 11, 4, 25]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25]

# --parity bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
		1, 58, 50, 42, 34, 26, 18,
		10, 2, 59, 51, 43, 35, 27,
		19, 11, 3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		7, 62, 54, 46, 38, 30, 22,
		14, 6, 61, 53, 45, 37, 29,
		21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts
shift_table = [1, 1, 2, 2,
                2, 2, 2, 2,
                1, 2, 2, 2,
                2, 2, 2, 1]

# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
			3, 28, 15, 6, 21, 10,
			23, 19, 12, 4, 26, 8,
			16, 7, 27, 20, 13, 2,
			41, 52, 31, 37, 47, 55,
			30, 40, 51, 45, 33, 48,
			44, 49, 39, 56, 34, 53,
			46, 42, 50, 36, 29, 32]


def ascii2bin(text):
	# Convert the string to binary
    binary_text = ''
    for char in text:
        binary_text += format(ord(char), '08b')
	# "".join([bin(ord(i))[2:].zfill(8) for i in st])
    return binary_text[:64].ljust(64, '0')

def bin2ascii(binary_text):
    # Разделяем бинарную строку на группы по 8 бит
    chars = [binary_text[i:i+8] for i in range(len(binary_text), 8)]
    # Преобразуем каждую группу в соответствующий ASCII-символ
    ascii_text = ''.join(chr(int(char, 2)) for char in chars)
    return ascii_text

# Binary to decimal conversion
def bin2dec(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

# Decimal to binary conversion
def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

# Permute function to rearrange the bits
def permute(k, arr, n):
	permutation = ""
	for i in range(n):
		permutation = permutation + k[arr[i] - 1]
	return permutation

# shifting the bits towards left by nth shifts
def shift_left(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1, len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

# calculating xow of two strings of binary number a and b
def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans

def adding_bits(key):
	bkey = ''
	s = 0
	i = 0
	for ind in range(1, 65):
		if ind in [8, 16, 24, 32, 40, 48, 56, 64]:
			if s == 0:
				bkey += '1'
			else:
				bkey += '0'
			s = 0
		else:
			bit = int(key[i:i+1])
			s ^= bit
			bkey += str(bit)
			i += 1
	return bkey

def encrypt(pt, key, encoding):
	if encoding == 'hex':
		pt = "".join([bin(int(i,16))[2:].zfill(4) for i in pt])
		key = "".join([bin(int(i,16))[2:].zfill(4) for i in key])
	elif encoding == 'ascii':
		pt = ascii2bin(pt)
		key = ascii2bin(key)
	
	key = adding_bits(key)
	# getting 56 bit key from 64 bit using the parity bits
	key = permute(key, keyp, 56)
	c = key[:28] # rkb for RoundKeys in binary
	d = key[28:] # rk for RoundKeys in hexadecimal

	rkb = []
	rk = []
	for i in range(16):
		# Shifting the bits by nth shifts by checking from shift table
		c = shift_left(c, shift_table[i])
		d = shift_left(d, shift_table[i])
		combine_str = c + d
		# Compression of key from 56 to 48 bits
		round_key = permute(combine_str, key_comp, 48)

		rkb.append(round_key)
		rk.append(bin2ascii(round_key))
	 
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
	return hex(int(cipher_text,2))[2:]


def decrypt(ct, key, encoding):
	if encoding == 'hex':
		ct = "".join([bin(int(i,16))[2:].zfill(4) for i in ct])
		key = "".join([bin(int(i,16))[2:].zfill(4) for i in key])
	elif encoding == 'ascii':
		ct = ascii2bin(ct)
		key = ascii2bin(key)
	
	key = adding_bits(key)
	# Getting the 56 bit key from 64 bit using the parity bits
	key = permute(key, keyp, 56)
	c = key[:28]  # Left half of the key
	d = key[28:]  # Right half of the key
	rkb = []
	rk = []
	for i in range(16):
		# Shifting the bits by nth shifts by checking from shift table
		c = shift_left(c, shift_table[i])
		d = shift_left(d, shift_table[i])
		combine_str = c + d
		# Compression of key from 56 to 48 bits
		round_key = permute(combine_str, key_comp, 48)
		rkb.append(round_key)
		rk.append(bin2ascii(round_key))

	# Initial Permutation
	ct = permute(ct, initial_perm, 64)

	# Splitting
	left = ct[:32]
	right = ct[32:]

	# Decryption rounds (using round keys in reverse order)
	for i in range(15, -1, -1):
		# Expansion D-box: Expanding the 32 bits data into 48 bits
		right_expanded = permute(right, exp_d, 48)

		# XOR RoundKey[i] and right_expanded
		xor_x = xor(right_expanded, rkb[i])

		# S-boxes: substituting the value from s-box table by calculating row and column
		sbox_str = ""
		for j in range(8):
			row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
			col = bin2dec(int(xor_x[j * 6 + 1:j * 6 + 5]))
			val = sbox[j][row][col]
			sbox_str += dec2bin(val)

		# Straight D-box: After substituting rearranging the bits
		sbox_str = permute(sbox_str, per, 32)

		# XOR left and sbox_str
		left = xor(left, sbox_str)

		# Swapper
		if i != 0:
			left, right = right, left

	# Combine left and right
	combine = left + right
	# Final permutation: final rearranging of bits to get plaintext
	plain_text_bin = permute(combine, final_perm, 64)

	# Convert binary to ASCII or Hex depending on encoding
	if encoding == 'ascii':
		plain_text = bin2ascii(plain_text_bin)  # Convert binary to ASCII
	else:
		plain_text = hex(int(plain_text_bin, 2))[2:]  # Convert binary to Hex

	return plain_text

def block_encrypt(pt, key, encoding):
	if encoding == 'hex':
		block_size = 16
	else:
		block_size = 8
	ciphertext = ""    
	for i in range(0, len(pt), block_size):
		block = pt[i:i+block_size]
		encrypted_block = encrypt(block, key, encoding)
		ciphertext += encrypted_block
    
	return ciphertext


def block_decrypt(ct, key, encoding):
	if encoding == 'hex':
		block_size = 16
	else:
		block_size = 8
	plaintext = ""
	for i in range(0, len(ct), block_size):
		block = ct[i:i+block_size]
		decrypted_block = decrypt(block, key, encoding)
		plaintext += decrypted_block
    
	return plaintext
'''
# Function to read content from a file
def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

# Function to write content to a file
def write_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)

# Modify encrypt and decrypt to include reading and writing keys and text from files

def encrypt_file(pt_file, key_file, encoding, output_file):
    # Read plaintext and key from files
    pt = read_file(pt_file)
    key = read_file(key_file)

    # Encrypt the text
    encrypted_text = block_encrypt(pt, key, encoding)

    # Write the encrypted text to the output file
    write_file(output_file, encrypted_text)
    print(f"Encrypted text saved to {output_file}")

def decrypt_file(ct_file, key_file, encoding, output_file):
    # Read ciphertext and key from files
    ct = read_file(ct_file)
    key = read_file(key_file)

    # Decrypt the text
    decrypted_text = block_decrypt(ct, key, encoding)

    # Write the decrypted text to the output file
    write_file(output_file, decrypted_text)
    print(f"Decrypted text saved to {output_file}")

'''
# make interaction with files
# avalanche effect function and 2 graphics (can be hex and ascii)
# functions for criteria