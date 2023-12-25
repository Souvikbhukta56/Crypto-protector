from .s_box import s_box
import numpy as np

class Key_expansion:
    def __init__(self, initial_key):
        self.initial_key = initial_key
        
    def g_function(self, word, round_constant):
        # Circular left shift
        word = np.concatenate((word[1:], word[:1]))
        # Substitute bytes
        for i in range(4):
            word[i] = s_box[word[i]]
        # XOR with round constant
        word[0] = word[0] ^ round_constant
        return word

    def get_key_schedule(self):
        key_schedule = np.zeros((11, 4, 4), dtype=int)

        round_constants = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        key_schedule[0] = self.initial_key

        for i in range(1, 11):
            for j in range(4):
                if j == 0:
                    g = self.g_function(key_schedule[i-1][3].copy(), round_constants[i])
                    key_schedule[i][j] = [g[k] ^ key_schedule[i-1][0][k] for k in range(4)]
                else:
                    key_schedule[i][j] = [key_schedule[i][j-1][k] ^ key_schedule[i-1][j][k] for k in range(4)]

        return key_schedule

