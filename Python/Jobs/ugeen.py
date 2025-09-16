from pathlib import Path

import pyperclip

# with Path("/home/mohamed/Downloads/code.txt").open("r") as e:
line = ""
with Path("/home/mohamed/Documents/datas/Databases/ugeens.txt").open("r") as lignes:
    for ligne in lignes:
        if cnt := ligne.strip():
            line = cnt

pyperclip.copy(line)
