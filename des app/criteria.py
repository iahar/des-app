import numpy as np
from alg_des import encrypt


# Генерация случайного бинарного вектора
def generate_random_vector(size):
    return np.random.randint(0, 2, size)

# Матрица зависимости (a_ij)
def calculate_dependency_matrix(input_vectors, output_vectors):
    n, m = input_vectors.shape[1], output_vectors.shape[1]
    dependency_matrix = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            dependency_matrix[i, j] = np.sum(input_vectors[:, i] != output_vectors[:, j])

    return dependency_matrix

# Матрица расстояний (b_ij)
def calculate_distance_matrix(input_vectors, output_vectors):
    n, m = input_vectors.shape[1], output_vectors.shape[1]
    distance_matrix = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            distance_matrix[i, j] = np.sum(np.bitwise_xor(input_vectors[:, i], output_vectors[:, j]))

    return distance_matrix

# 1. Среднее число измененных битов (d1)
def calculate_d1(distance_matrix, U_size):
    n, m = distance_matrix.shape
    return np.sum(distance_matrix) / (n * U_size)

# 2. Степень полноты преобразования (d2)
def calculate_d2(dependency_matrix):
    n, m = dependency_matrix.shape
    zeros_count = np.sum(dependency_matrix == 0)
    return 1 - zeros_count / (n * m)

# 3. Степень лавинного эффекта (d3)
def calculate_d3(distance_matrix, m):
    n, m = distance_matrix.shape
    return 1 - np.sum(np.abs(2 * distance_matrix - m)) / (n * m)

# 4. Степень соответствия строгому лавинному критерию (d4)
def calculate_d4(dependency_matrix, N):
    n, m = dependency_matrix.shape
    return 1 - np.sum(np.abs(2 * dependency_matrix - N)) / (n * m)


def calculate():
    n, m = 64, 56  # Размерность входных и выходных векторов
    U_size = 100  # Мощность множества U

    # Генерация случайных входных векторов
    input_vectors = np.array([generate_random_vector(n) for _ in range(U_size)])
    key = generate_random_vector(m)
    key_str = ''.join([str(x) for x in key])
    
    # Генерация выходных векторов с помощью блочного шифрования
    output_vectors = []
    for v in input_vectors:
        # Шифруем входной вектор и преобразуем его в двоичный вид
        encrypted_value = encrypt(''.join([str(x) for x in v]), key_str, 'bin')
        # Преобразуем зашифрованное значение в двоичный массив длиной m
        encrypted_bits = [int(bit) for bit in bin(int(encrypted_value, 16))[2:].zfill(n)]
        output_vectors.append(encrypted_bits)

    output_vectors = np.array(output_vectors)

    # Матрицы зависимости и расстояний
    dependency_matrix = calculate_dependency_matrix(input_vectors, output_vectors)
    distance_matrix = calculate_distance_matrix(input_vectors, output_vectors)

    # Расчет критериев
    d1 = calculate_d1(distance_matrix, U_size)
    d2 = calculate_d2(dependency_matrix)
    d3 = calculate_d3(distance_matrix, m)
    d4 = calculate_d4(dependency_matrix, U_size)

    print(f"d1 (Среднее число измененных битов): {d1}")
    print(f"d2 (Степень полноты преобразования): {d2}")
    print(f"d3 (Степень лавинного эффекта): {d3}")
    print(f"d4 (Степень соответствия строгому лавинному критерию): {d4}")





