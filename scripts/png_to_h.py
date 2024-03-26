# *************************************************************************
#
# Copyright (c) 2024 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.  
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

import os
import numpy as np
from PIL import Image

DEFINE_PREFIX = "UNIFACE_"
header_list = []

def png_to_c_header(png_filename, out_dir):
    
    # Getting a grey numpy array
    img = Image.open(png_filename)
    img = img.convert('L') # to gray
    png_arr = np.array(img)
    
    file_name_base = png_filename.split("/")[-1].split(".")[0]
    
    # Header #define name
    define_name = DEFINE_PREFIX + (file_name_base.replace("-", "_")
                                   .replace(".", "_")
                                   .replace(" ", "_")
                                   .upper())
    
    header_path = f"{out_dir}/{file_name_base}.h"
    with open(header_path, 'w') as f:
        f.write("#pragma once\n\n")
        f.write(f"#define {define_name} \\\n")
        f.write("{\\\n")
        
        # The last value to determine where to end the array
        last_row = len(png_arr) - 1
        last_col = len(png_arr[0]) - 1
        
        row_cur = 0  # tmp
        for row in png_arr:
            f.write("	")
            col_cur = 0  # tmp
            byte_cur = 0
            byte_val = 0
            bit_cur = 0 # bit counter in byte
            for pixel_val in row:
                bit = 0
                if (255 - pixel_val) > 128: # check inverted value
                    bit = 1
                    
                byte_val = (byte_val << 1) | bit
                
                 # finish the byte
                if bit_cur == 7:
                    # write reverted bits in byte 
                    byte_val = int('{:08b}'.format(byte_val)[::-1], 2)
                
                    if row_cur == last_row and col_cur == last_col:
                        # no comma for the last element
                        f.write(f"{byte_val:#04x}")
                    else:
                        f.write(f"{byte_val:#04x}, ")
                    byte_cur += 1 # next byte
                    byte_val = 0
                    bit_cur = 0
                # or continue
                else: 
                    bit_cur += 1
                col_cur += 1  # tmp
            f.write("\\\n")
            row_cur += 1  # tmp
        
        f.write("}\n\n")
    return f"{file_name_base}.h"


if __name__ == "__main__":
    # Repo root
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    
    # For all png in export/png folder, convert to C header
    png_dir = "png"
    out_dir = "h"
    
    # Create export/h folder if not exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # Clear the old headers if there are
    for h in os.listdir(out_dir):
        if h.endswith(".h"):
            os.remove(f"{out_dir}/{h}")
    
    # Convert all png to C headers
    for png in os.listdir(png_dir):
        if png.endswith(".png"):
            new_h = png_to_c_header(f"{png_dir}/{png}", out_dir)
            header_list.append(new_h)
            
    # Create a unifaces header file
    if not os.path.exists("include"):
        os.makedirs("include")
    with open(f"include/unifaces.h", 'w') as f:
        for h in header_list:
            f.write(f"#include \"../h/{h}\"\n")
        f.write("\n")
        f.write("#define UNIFACE_WIDTH 128\n")
        f.write("#define UNIFACE_HEIGHT 64\n")
