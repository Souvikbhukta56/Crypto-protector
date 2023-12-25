import numpy as np

def mixcolumns_inv(state):
    # Define the inverse MixColumns matrix in 8-bit form
    inv_mix_columns_matrix = [
        [0x0E, 0x0B, 0x0D, 0x09],
        [0x09, 0x0E, 0x0B, 0x0D],
        [0x0D, 0x09, 0x0E, 0x0B],
        [0x0B, 0x0D, 0x09, 0x0E]
    ]

    # Initialize a new state matrix for the result
    new_state = np.zeros((4, 4), dtype=int)

    for col in range(4):
        for row in range(4):
            result = 0x00
            for i in range(4):
                result ^= aes_multiply(inv_mix_columns_matrix[row][i], state[i][col])
            new_state[row][col] = result & 0xFF  # Limit the result to 8 bits

    return new_state

def aes_multiply(a, b):
    # Multiply two numbers in GF(2^8)
    result = 0x00
    for _ in range(8):
        if b & 0x01:
            result ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x1B  # XOR with the AES irreducible polynomial (0x11B) for modulo reduction
        b >>= 1
    return result & 0xFF  # Limit the result to 8 bits

# print(aes_inverse_mix_columns([['23', '39', '79', '17'], ['23', '0b', 'db', '2f'], ['80', '70', '33', '0d'], ['5c', '74', 'a8', '40']]))