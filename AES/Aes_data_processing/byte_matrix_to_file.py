import os

def byte_matrix_to_file(byte_matrix, output_file_path):
    # Opening the file in binary write mode
    with open(output_file_path, 'wb') as file:
        for i in byte_matrix:
            for j in i:
                for k in j:
                    # Convert the hexadecimal value back to its binary form
                    byte = bytes.fromhex('0x{:02x}'.format(k)[2:])
                    # Write the byte to the output file
                    file.write(byte)
    