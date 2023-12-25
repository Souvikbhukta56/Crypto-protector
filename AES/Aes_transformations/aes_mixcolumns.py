import numpy as np
def mixcolumns(state):
    # Define the fixed MixColumns matrix in 8-bit form
    mix_columns_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    # Initialize a new state matrix for the result
    new_state = np.zeros((4, 4), dtype=int)

    for col in range(4):
        for row in range(4):
            result = 0x00
            for i in range(4):
                result ^= aes_multiply(mix_columns_matrix[row][i], state[i][col])
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
    return result & 0xFF 

# print(mixcolumns(np.array([[27, 198 , 83, 132],
#  [ 97, 161 ,230 , 53],
#  [211 ,210  , 7, 239],
#  [179 ,113  ,86, 163]])))

#  [[245 204 198   0]
#  [  4 131 219 103]
#  [  9  75  65 138]
#  [226 192 184  16]]