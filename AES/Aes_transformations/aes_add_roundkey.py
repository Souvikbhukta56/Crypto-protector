import numpy as np
def add_roundkey(state_array, round_key):
    return np.bitwise_xor(state_array, round_key)
    
