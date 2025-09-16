import os

os.chdir("/home/mohamed/Documents/Files/Works/2023-2024/Tests diagnostiques")

for f in os.listdir():
    if not os.path.exists(f.replace('.odt', 'pdf')):
        cmd = f"libreoffice --convert-to pdf '{f}'"
        os.system(cmd)
