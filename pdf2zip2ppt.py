import os
import subprocess
import re
import zipfile
import shutil

pattern_list = ['C18_male', 'C18_female', 'C19-20_female', 'C19-20_female', 'C18-20_female', 'C18-20_female']

for file_pattern in pattern_list:


    dir_zip = 'zip'
    dir_pdf = 'pdf'
    dir_png = 'png'
    density = '200'


    path_zip=dir_zip + '/'+file_pattern+'.zip'
    dir_base = "C:/project/Occasional/240625_freddie_colorectum/_figs"

    with zipfile.ZipFile(path_zip, 'w') as zip_ref:
        # convert to zip
        for file_base in os.listdir(dir_base):
            if re.search(file_pattern, file_base):
                zip_ref.write(os.path.join(dir_base, file_base), file_base)


    # drop PDF and PNG here
    for file_base in os.listdir(dir_pdf):
        if re.search(".pdf", file_base):
            file_path = os.path.join(dir_pdf, file_base)
            os.remove(file_path)

    for file_base in os.listdir(dir_png):
        if re.search(".png", file_base):
            file_path = os.path.join(dir_png, file_base)
            os.remove(file_path)

    with zipfile.ZipFile(path_zip, 'r') as zip_ref:
        zip_ref.extractall(dir_pdf)


    for file_base in os.listdir(dir_pdf):

        if re.search(".pdf", file_base):
            file_png =  file_base.replace(".pdf", ".png")
            path_base = os.path.join(dir_base, file_base)
            path_png = os.path.join(dir_png, file_png)
            subprocess.call(['magick','-density', density,  path_base,'-resize', '100%',   '-compress','lzw', '-background','white', '-alpha','remove', path_png], shell=True)
            print(file_png)


    subprocess.call(['node','pdf2ppt.js', file_pattern], shell=True)

