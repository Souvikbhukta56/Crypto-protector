import numpy as np

def file_to_byte_matrix(file_object):
    byte_matrix = []
    for i in range(0, len(file_object), 16): 
        try:
            row = np.reshape(list(file_object[i:i+16]),(4,4))
            byte_matrix.append(row)
        except:
            row = np.reshape(list(file_object[i:])+[0 for _ in range(16-len(file_object)+i)],(4,4))
    return byte_matrix
    
            
        
    

