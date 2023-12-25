import numpy as np

def generate_key():
    return np.random.randint(0, 256, size=(4, 4), dtype=np.uint8)



