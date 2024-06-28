import os
import subprocess
import re

dir_base = 'pdf'
dir_png = 'png'


#for all pdf
for file_base in os.listdir(dir_base):

    if re.search(".pdf", file_base):
        file_png =  file_base.replace(".pdf", ".png")
        path_base = os.path.join(dir_base, file_base)
        path_png = os.path.join(dir_png, file_png)
        subprocess.call(['magick','-density', '200',  path_base,'-resize', '100%',   '-compress','lzw', '-background','white', '-alpha','remove', path_png], shell=True)
        print(file_png)








