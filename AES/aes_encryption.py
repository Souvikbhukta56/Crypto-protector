from .Aes_transformations.aes_subbytes import subbytes
from .Aes_transformations.aes_shiftrows import shiftrows
from .Aes_transformations.aes_mixcolumns import mixcolumns
from .Aes_transformations.aes_add_roundkey import add_roundkey

from .Aes_constants.s_box import s_box
import numpy   

class Encryption:
    def __init__(self, key_schedule):
        self.key_schedule = key_schedule

    def encrypt(self, file_data):
        ciphertext = []
        
        for data in file_data:
            # Initial transformation
            state_array = add_roundkey(data, self.key_schedule[0])
            
            # Round 1 to 9
            for i in range(1, 10):
                state_array = subbytes(state_array, s_box)
                state_array = shiftrows(state_array)
                state_array = mixcolumns(state_array)
                state_array = add_roundkey(state_array, self.key_schedule[i])
            
            # Final Round 
            state_array = subbytes(state_array, s_box)
            state_array = shiftrows(state_array)
            state_array = add_roundkey(state_array, self.key_schedule[10])
            
            ciphertext.append(state_array.tolist())
        return ciphertext

