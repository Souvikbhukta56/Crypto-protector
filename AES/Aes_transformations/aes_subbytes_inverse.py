import numpy as np

def subbytes_inv(state_array, s_box_inv):
    for i in range(4):
        for j in range(4):
            state_array[i][j] = s_box_inv[state_array[i][j]]
    return state_array

