import os
import numpy as np
from PIL import Image

DEFINE_PREFIX = "UNIFACE_"
header_list = []


def png_to_c_header(png_filename, out_dir):
    
    img = Image.open(png_filename)
    img = img.convert('L') # to gray
    
    png_arr = np.array(img)
    
    file_name_base = png_filename.split("/")[-1].split(".")[0]
    
    define_name = DEFINE_PREFIX + (file_name_base.replace("-", "_")
                                   .replace(".", "_")
                                   .replace(" ", "_")
                                   .upper())
    
    header_path = f"{out_dir}/{file_name_base}.h"
    with open(header_path, 'w') as f:
        f.write("#pragma once\n\n")
        f.write(f"#define {define_name} \\\n")
        f.write("{\\\n")
        
        for row in png_arr:
            for pixel in row:
                val = hex(255 - pixel)
                f.write(f"{val}, ")
            f.write("\\\n")
        
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
