from .Aes_transformations.aes_subbytes_inverse import subbytes_inv
from .Aes_transformations.aes_shiftrows_inverse import shiftrows_inv
from .Aes_transformations.aes_mixcolumns_inverse import mixcolumns_inv
from .Aes_transformations.aes_add_roundkey import add_roundkey
from .Aes_constants.s_box_inverse import s_box_inv

class Decryption:
    def __init__(self, key_schedule):
        self.key_schedule = key_schedule

    def decrypt(self, ciphertext):
        original_data = []
        
        for data in ciphertext:
            state_array = add_roundkey(data, self.key_schedule[-1])
            state_array = shiftrows_inv(state_array)
            state_array = subbytes_inv(state_array, s_box_inv)

            for i in range(1, 10):
                state_array = add_roundkey(state_array, self.key_schedule[-i-1])
                state_array = mixcolumns_inv(state_array)
                state_array = shiftrows_inv(state_array)
                state_array = subbytes_inv(state_array, s_box_inv)
            
            state_array = add_roundkey(state_array, self.key_schedule[0])
            original_data.append(state_array)
        return original_data