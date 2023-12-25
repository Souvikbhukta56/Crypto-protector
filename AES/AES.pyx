import numpy as np
cimport numpy as np

cdef class AES:
    cdef dict[int, int] s_box 
    cdef dict[int, int] s_box_inv
    def __cinit__(self):
        self.s_box = {
        0: 99, 1: 124, 2: 119, 3: 123, 4: 242, 5: 107, 6: 111, 7: 197, 8: 48, 9: 1, 10: 103, 11: 43, 12: 254, 
        13: 215, 14: 171, 15: 118, 16: 202, 17: 130, 18: 201, 19: 125, 20: 250, 21: 89, 22: 71, 23: 240, 24: 173, 
        25: 212, 26: 162, 27: 175, 28: 156, 29: 164, 30: 114, 31: 192, 32: 183, 33: 253, 34: 147, 35: 38, 36: 54, 
        37: 63, 38: 247, 39: 204, 40: 52, 41: 165, 42: 229, 43: 241, 44: 113, 45: 216, 46: 49, 47: 21, 48: 4, 
        49: 199, 50: 35, 51: 195, 52: 24, 53: 150, 54: 5, 55: 154, 56: 7, 57: 18, 58: 128, 59: 226, 60: 235, 61: 39,
        62: 178, 63: 117, 64: 9, 65: 131, 66: 44, 67: 26, 68: 27, 69: 110, 70: 90, 71: 160, 72: 82, 73: 59, 74: 214,
        75: 179, 76: 41, 77: 227, 78: 47, 79: 132, 80: 83, 81: 209, 82: 0, 83: 237, 84: 32, 85: 252, 86: 177, 
        87: 91, 88: 106, 89: 203, 90: 190, 91: 57, 92: 74, 93: 76, 94: 88, 95: 207, 96: 208, 97: 239, 98: 170, 
        99: 251, 100: 67, 101: 77, 102: 51, 103: 133, 104: 69, 105: 249, 106: 2, 107: 127, 108: 80, 109: 60, 
        110: 159, 111: 168, 112: 81, 113: 163, 114: 64, 115: 143, 116: 146, 117: 157, 118: 56, 119: 245, 120: 188, 
        121: 182, 122: 218, 123: 33, 124: 16, 125: 255, 126: 243, 127: 210, 128: 205, 129: 12, 130: 19, 131: 236, 
        132: 95, 133: 151, 134: 68, 135: 23, 136: 196, 137: 167, 138: 126, 139: 61, 140: 100, 141: 93, 142: 25, 
        143: 115, 144: 96, 145: 129, 146: 79, 147: 220, 148: 34, 149: 42, 150: 144, 151: 136, 152: 70, 153: 238, 
        154: 184, 155: 20, 156: 222, 157: 94, 158: 11, 159: 219, 160: 224, 161: 50, 162: 58, 163: 10, 164: 73, 
        165: 6, 166: 36, 167: 92, 168: 194, 169: 211, 170: 172, 171: 98, 172: 145, 173: 149, 174: 228, 175: 121, 
        176: 231, 177: 200, 178: 55, 179: 109, 180: 141, 181: 213, 182: 78, 183: 169, 184: 108, 185: 86, 186: 244, 
        187: 234, 188: 101, 189: 122, 190: 174, 191: 8, 192: 186, 193: 120, 194: 37, 195: 46, 196: 28, 197: 166, 
        198: 180, 199: 198, 200: 232, 201: 221, 202: 116, 203: 31, 204: 75, 205: 189, 206: 139, 207: 138, 208: 112, 
        209: 62, 210: 181, 211: 102, 212: 72, 213: 3, 214: 246, 215: 14, 216: 97, 217: 53, 218: 87, 219: 185, 
        220: 134, 221: 193, 222: 29, 223: 158, 224: 225, 225: 248, 226: 152, 227: 17, 228: 105, 229: 217, 230: 142, 
        231: 148, 232: 155, 233: 30, 234: 135, 235: 233, 236: 206, 237: 85, 238: 40, 239: 223, 240: 140, 241: 161, 
        242: 137, 243: 13, 244: 191, 245: 230, 246: 66, 247: 104, 248: 65, 249: 153, 250: 45, 251: 15, 252: 176, 
        253: 84, 254: 187, 255: 22
    }
        self.s_box_inv = {
        99: 0, 124: 1, 119: 2, 123: 3, 242: 4, 107: 5, 111: 6, 197: 7, 48: 8, 1: 9, 103: 10, 43: 11, 
        254: 12, 215: 13, 171: 14, 118: 15, 202: 16, 130: 17, 201: 18, 125: 19, 250: 20, 89: 21, 71: 22, 240: 23, 
        173: 24, 212: 25, 162: 26, 175: 27, 156: 28, 164: 29, 114: 30, 192: 31, 183: 32, 253: 33, 147: 34, 38: 35, 
        54: 36, 63: 37, 247: 38, 204: 39, 52: 40, 165: 41, 229: 42, 241: 43, 113: 44, 216: 45, 49: 46, 21: 47, 4: 48, 
        199: 49, 35: 50, 195: 51, 24: 52, 150: 53, 5: 54, 154: 55, 7: 56, 18: 57, 128: 58, 226: 59, 235: 60, 39: 61, 
        178: 62, 117: 63, 9: 64, 131: 65, 44: 66, 26: 67, 27: 68, 110: 69, 90: 70, 160: 71, 82: 72, 59: 73, 214: 74, 
        179: 75, 41: 76, 227: 77, 47: 78, 132: 79, 83: 80, 209: 81, 0: 82, 237: 83, 32: 84, 252: 85, 177: 86, 91: 87, 
        106: 88, 203: 89, 190: 90, 57: 91, 74: 92, 76: 93, 88: 94, 207: 95, 208: 96, 239: 97, 170: 98, 251: 99, 
        67: 100, 77: 101, 51: 102, 133: 103, 69: 104, 249: 105, 2: 106, 127: 107, 80: 108, 60: 109, 159: 110, 168: 111, 
        81: 112, 163: 113, 64: 114, 143: 115, 146: 116, 157: 117, 56: 118, 245: 119, 188: 120, 182: 121, 218: 122, 
        33: 123, 16: 124, 255: 125, 243: 126, 210: 127, 205: 128, 12: 129, 19: 130, 236: 131, 95: 132, 151: 133, 
        68: 134, 23: 135, 196: 136, 167: 137, 126: 138, 61: 139, 100: 140, 93: 141, 25: 142, 115: 143, 96: 144, 
        129: 145, 79: 146, 220: 147, 34: 148, 42: 149, 144: 150, 136: 151, 70: 152, 238: 153, 184: 154, 20: 155, 
        222: 156, 94: 157, 11: 158, 219: 159, 224: 160, 50: 161, 58: 162, 10: 163, 73: 164, 6: 165, 36: 166, 92: 167, 
        194: 168, 211: 169, 172: 170, 98: 171, 145: 172, 149: 173, 228: 174, 121: 175, 231: 176, 200: 177, 55: 178, 
        109: 179, 141: 180, 213: 181, 78: 182, 169: 183, 108: 184, 86: 185, 244: 186, 234: 187, 101: 188, 122: 189, 
        174: 190, 8: 191, 186: 192, 120: 193, 37: 194, 46: 195, 28: 196, 166: 197, 180: 198, 198: 199, 232: 200, 
        221: 201, 116: 202, 31: 203, 75: 204, 189: 205, 139: 206, 138: 207, 112: 208, 62: 209, 181: 210, 102: 211, 
        72: 212, 3: 213, 246: 214, 14: 215, 97: 216, 53: 217, 87: 218, 185: 219, 134: 220, 193: 221, 29: 222, 158: 223, 
        225: 224, 248: 225, 152: 226, 17: 227, 105: 228, 217: 229, 142: 230, 148: 231, 155: 232, 30: 233, 135: 234, 
        233: 235, 206: 236, 85: 237, 40: 238, 223: 239, 140: 240, 161: 241, 137: 242, 13: 243, 191: 244, 230: 245, 
        66: 246, 104: 247, 65: 248, 153: 249, 45: 250, 15: 251, 176: 252, 84: 253, 187: 254, 22: 255
    }

    def generate_key(self) -> np.uint8_t[:, :]:
        return np.random.randint(0, 256, size=(4, 4), dtype='unsigned char')

    def g_function(self, np.uint8_t[:] word, int round_constant) -> np.uint8_t[:]:
        w = np.concatenate((word[1:], word[:1]))
        for i in range(4):
            w[i] = self.s_box[w[i]]
        w[0] = w[0] ^ round_constant
        return w

    def get_key_schedule(self, np.uint8_t[:, :] AES_KEY) -> np.uint8_t[:, :, :]:
        key_schedule = np.zeros((11, 4, 4), dtype=int)
        round_constants = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        key_schedule[0] = AES_KEY
        for i in range(1, 11):
            for j in range(4):
                if j == 0:
                    g = self.g_function(key_schedule[i-1][3].copy(), round_constants[i])
                    key_schedule[i][j] = [g[k] ^ key_schedule[i-1][0][k] for k in range(4)]
                else:
                    key_schedule[i][j] = [key_schedule[i][j-1][k] ^ key_schedule[i-1][j][k] for k in range(4)]
        return key_schedule

    def add_roundkey(np.uint8_t[:, :] state_array, np.uint8_t[:, :] round_key) -> np.uint8_t[:, :]:
        return np.bitwise_xor(state_array, round_key)
    
    def shiftrows(np.uint8_t[:, :] state_array) -> np.uint8_t[:, :]:
        state_array[1] = np.concatenate((state_array[1][1:], state_array[1][:1]))
        state_array[2] = np.concatenate((state_array[2][2:], state_array[2][:2]))
        state_array[3] = np.concatenate((state_array[3][3:], state_array[3][:3]))
        return state_array
    
    def shiftrows_inv(np.uint8_t[:, :] state_array) -> np.uint8_t[:, :]:
        state_array[1] = np.concatenate((state_array[1][-1:], state_array[1][:-1]))
        state_array[2] = np.concatenate((state_array[2][-2:], state_array[2][:-2]))
        state_array[3] = np.concatenate((state_array[3][-3:], state_array[3][:-3]))
        return state_array

    def subbytes(self, np.uint8_t[:, :] state_array) -> np.uint8_t[:, :]:
        for i in range(4):
            for j in range(4):
                state_array[i][j] = self.s_box[state_array[i][j]]
        return state_array
    
    def subbytes_inv(self, np.uint8_t[:, :] state_array) -> np.uint8_t[:, :]:
        for i in range(4):
            for j in range(4):
                state_array[i][j] = self.s_box_inv[state_array[i][j]]
        return state_array
    
    def mixcolumns(np.uint8_t[:, :] state_array) -> np.uint8_t[:, :]:
        def aes_multiply(int a, int b) -> int:
            result = 0x00
            for _ in range(8):
                if b & 0x01:
                    result ^= a
                high_bit_set = a & 0x80
                a <<= 1
                if high_bit_set:
                    a ^= 0x1B
                b >>= 1
            return result & 0xFF 

        mix_columns_matrix = np.array([
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ], dtype='unsigned char')
        new_state = np.zeros((4, 4), dtype='unsigned char')
        for col in range(4):
            for row in range(4):
                result = 0x00
                for i in range(4):
                    result ^= aes_multiply(mix_columns_matrix[row][i], state_array[i][col])
                new_state[row][col] = result & 0xFF
        return new_state

    def mixcolumns_inv(np.uint8_t[:, :] state_array) -> np.uint8_t[:, :]:
        def aes_multiply(int a, int b) -> int:
            result = 0x00
            for _ in range(8):
                if b & 0x01:
                    result ^= a
                high_bit_set = a & 0x80
                a <<= 1
                if high_bit_set:
                    a ^= 0x1B
                b >>= 1
            return result & 0xFF

        inv_mix_columns_matrix = np.array([
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        ], dtype='unsigned char')
        new_state = np.zeros((4, 4), dtype='unsigned char')
        for col in range(4):
            for row in range(4):
                result = 0x00
                for i in range(4):
                    result ^= aes_multiply(inv_mix_columns_matrix[row][i], state_array[i][col])
                new_state[row][col] = result & 0xFF 
        return new_state

    def file_to_byte_matrix(file_object) -> list[np.uint8_t[:, :]]:
        byte_matrix = []
        for i in range(0, len(file_object), 16): 
            try:
                row = np.reshape(list(file_object[i:i+16]),(4,4))
                byte_matrix.append(row)
            except:
                row = np.reshape(list(file_object[i:])+[0 for _ in range(16-len(file_object)+i)],(4,4))
        return byte_matrix
    
    def byte_matrix_to_file(list[np.uint8_t[:, :]] byte_matrix, str output_file_path):
        with open(output_file_path, 'wb') as file:
            for i in byte_matrix:
                for j in i:
                    for k in j:
                        byte = bytes.fromhex('0x{:02x}'.format(k)[2:])
                        file.write(byte)
    
    def encrypt(self, file_object) -> list[np.uint8_t[:, :]]:
        file_data = self.file_to_byte_matrix(file_object)
        ciphertext = []
        AES_KEY = self.generate_key()
        key_schedule = self.get_key_schedule(AES_KEY)
        for data in file_data:
            state_array = self.add_roundkey(data, key_schedule[0])
            for i in range(1, 10):
                state_array = self.subbytes(state_array)
                state_array = self.shiftrows(state_array)
                state_array = self.mixcolumns(state_array)
                state_array = self.add_roundkey(state_array, key_schedule[i])
            state_array = self.subbytes(state_array)
            state_array = self.shiftrows(state_array)
            state_array = self.add_roundkey(state_array, key_schedule[10])
            ciphertext.append(state_array)
        ciphertext.append(AES_KEY)
        return ciphertext
    
    def decrypt(self, list[np.uint8_t[:, :]] ciphertext, str file_name):
        AES_KEY = ciphertext[-1]
        key_schedule = self.get_key_schedule(AES_KEY)
        original_data = []
        for data in ciphertext[:-1]:
            state_array = self.add_roundkey(data, key_schedule[-1])
            state_array = self.shiftrows_inv(state_array)
            state_array = self.subbytes_inv(state_array)
            for i in range(1, 10):
                state_array = self.add_roundkey(state_array, self.key_schedule[-i-1])
                state_array = self.mixcolumns_inv(state_array)
                state_array = self.shiftrows_inv(state_array)
                state_array = self.subbytes_inv(state_array)
            state_array = self.add_roundkey(state_array, self.key_schedule[0])
            original_data.append(state_array)
        self.byte_matrix_to_file(original_data, file_name)
        return original_data