import json
from pathlib import Path
import re


def gad(line, nb=0):
    nts = re.findall(r"\[([0-9]+:[0-9]+\.[0-9]+)\]", line)
    for nt in nts:
        ms = fetch(nt)
        if ms == 0:
            continue
        nb = int(ms + nb)
        line = line.replace(f"[{nt}]", f"[{format(nb)}]")

    return line


def fetch(t):
    nbs = [float(nb) for nb in t.split(":")]
    return sum(nb * (60**i) for i, nb in enumerate(nbs[::-1])) * 100


def format(ss):
    ms = ss % 100
    ms = f"{int(ms):02}"
    nbs = []
    ss = ss // 100
    while ss > 0:
        nbs.append(f"{ss % 60:02}")
        ss = ss // 60
    while len(nbs) < 2:
        nbs.append("00")
    f = ":".join(nbs[::-1])
    return f"{f}.{ms}"


def parseAll(parent):
    for filename in parent.glob("*.lrc"):
        fn = filename.stem
        bfile = Path(f"Backups/{fn}.json")

        # if bfile.exists():
        #     continue
        with open(filename, "r") as el:
            lines = el.readlines()
        if not bfile.exists():
            with open(bfile, "w") as fl:
                json.dump(lines, fl)
        load(filename)


def load(filename, nb=0):
    with open(filename, "r") as el:
        lines = el.readlines()

    new_lrc = []

    zero_found = False

    for line in lines:
        line = line.strip()
        if re.match(r"^\[[0-9].+]$", line):
            line += "~~~~~~~~~"
        if re.match(r"^\[[0-9]", line):
            if not zero_found:
                if not re.match(r"\[00:00", line):
                    new_lrc.append("[00:00]~~~~~~~~~")
                zero_found = True
            line = gad(line, nb)
        new_lrc.append(line)

    with open(filename, "w") as el:
        el.write("\n".join(new_lrc))


# 1059498802
parent = Path("/home/mohamed/Documents/OSD")
parseAll(parent)
