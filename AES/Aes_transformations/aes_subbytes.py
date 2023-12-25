def subbytes(state_array, s_box):
    for i in range(4):
        for j in range(4):
            state_array[i][j] = s_box[state_array[i][j]]

    return state_array

