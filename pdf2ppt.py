import os
import subprocess
import re
import zipfile
import shutil


dir_base = 'pdf'
dir_png = 'png'
dir_zip = 'zip'
bool_pdf = True;
bool_zip = True 
density = '200'


if bool_zip:
    for file_base in os.listdir(dir_zip):
        if re.search(".zip", file_base):

            # update pptx name
            pptx_name =  file_base.replace(".zip","")
            path_zip = os.path.join(dir_zip, file_base)
            if bool_pdf:
                # unzip to folder
                for file_base in os.listdir(dir_base):
                    if re.search(".pdf", file_base):
                        file_path = os.path.join(dir_base, file_base)
                        os.remove(file_path)

                with zipfile.ZipFile(path_zip, 'r') as zip_ref:
                    zip_ref.extractall(dir_base)

            else:
                for file_base in os.listdir(dir_png):
                    if re.search(".png", file_base):
                        file_path = os.path.join(dir_png, file_base)
                        os.remove(file_path)

                with zipfile.ZipFile(path_zip, 'r') as zip_ref:
                    zip_ref.extractall(dir_png)


if bool_pdf:
    for file_base in os.listdir(dir_base):

        if re.search(".pdf", file_base):
            file_png =  file_base.replace(".pdf", ".png")
            path_base = os.path.join(dir_base, file_base)
            path_png = os.path.join(dir_png, file_png)
            subprocess.call(['magick','-density', density,  path_base,'-resize', '100%',   '-compress','lzw', '-background','white', '-alpha','remove', path_png], shell=True)
            print(file_png)


subprocess.call(['node','pdf2ppt.js', pptx_name], shell=True)

