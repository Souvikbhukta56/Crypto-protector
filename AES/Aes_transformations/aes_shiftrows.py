import numpy as np

def shiftrows(state_array):
    # Don't need to shift 1st row

    # Shifting 2nd row by 1 place left
    state_array[1] = np.concatenate((state_array[1][1:], state_array[1][:1]))

    # Shifting 3rd row by 2 place left
    state_array[2] = np.concatenate((state_array[2][2:], state_array[2][:2]))

    # Shifting 4th row by 3 place left
    state_array[3] = np.concatenate((state_array[3][3:], state_array[3][:3]))

    return state_array

