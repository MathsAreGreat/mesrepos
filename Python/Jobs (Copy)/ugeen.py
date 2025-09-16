import pyperclip

with open("/home/mohamed/Documents/datas/Databases/ugeens.txt", "r") as e:
    lines = e.readlines()
for line in lines[-2:]:
    print(line.strip())
pyperclip.copy(line.strip())
