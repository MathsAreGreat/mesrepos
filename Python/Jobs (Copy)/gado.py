from pathlib import Path
import re
import zipfile
import shutil


def remove_empty_directories(top_directory):
    nb = 1
    while nb > 0:
        nb = 0
        top_directory_path = Path(top_directory)
        for dir_path in top_directory_path.rglob("*"):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                print(f"> Removing empty directory: {dir_path}")
                dir_path.rmdir()
                nb += 1


t_parent = Path("/home/mohamed/Videos/Torrents")
m_parent = t_parent / "Movies"

for doc in m_parent.glob("*"):
    files = list(doc.glob("*.jpg")) + list(doc.glob("*.txt"))
    if files:
        for f in doc.glob("*.srt"):
            f.unlink()
        for f in doc.glob("*.ass"):
            f.unlink()

infos = {}
pp = Path("/home/mohamed/Downloads")
for f in pp.glob("*zip"):
    if "_arabic-" in f.stem:
        shutil.move(f, pp / "Files/Zips" / f.name)

for f in t_parent.rglob("*"):
    if f.is_file():
        if f.suffix in [".jpg", ".txt", ".png"]:
            f.unlink()
        elif "'" in f.stem or " " in f.stem:
            name = ".".join(e for e in f.stem.replace("'", "").split(" ") if e)
            name = name.title().replace("0P.", "0p.")
            f.rename(f.with_stem(name))

files = []
for doc in m_parent.glob("*/Subs/*ara*"):
    files.append(doc)

for f in files:
    doc = f.parent.parent
    sl = None
    content = ""
    for fl in doc.glob("*.*"):
        if fl.suffix == ".mp4":
            sl = fl.with_suffix(".srt")
            with open(f, "r") as file:
                content = file.read()
        else:
            s = fl.stem
            tl = fl.parent / "Subs" / fl.name
            fl.rename(tl)
    if sl:
        with open(sl, "w") as file:
            file.write(content)

for pf in m_parent.glob("*/Subs"):
    tf = pf.with_name("Temps")
    pf.rename(tf)

for doc in m_parent.glob("*/Temps"):
    shutil.rmtree(doc)


films = {}
for f in list(t_parent.rglob("*.mkv"))+list(t_parent.rglob("*.mp4")):
    if not re.search(r"S[0-9]+\.?E[0-9]+", f.stem, flags=re.IGNORECASE):
        key = re.sub(r"\.[0-9]+p\..+$", r"", f.stem)
        ends = key.split(".")
        if re.search(r"^[0-9]+$", ends[-1]):
            key = ".".join(ends[:-1])
    else:
        name, s, e = re.findall(
            r"^(.+)S([0-9]+)\.?E([0-9]+)",
            f.stem,
            flags=re.IGNORECASE
        )[0]
        key = f"{name}s{int(s):02}.e{int(e):02}"
    key = key.lower()
    films[key] = f

z_parent = Path("/home/mohamed/Downloads/Files/Zips")
s_parent = Path("/home/mohamed/Downloads/Files/Srts")
s_parent.mkdir(
    parents=True,
    exist_ok=True
)

for file_from in Path("/home/mohamed/Downloads/Files/Zips").glob("*zip"):
    if "_arabic-" not in file_from.stem:
        continue
    file_to = s_parent / file_from.stem
    if file_to.exists():
        continue
    with zipfile.ZipFile(file_from, "r") as zip_ref:
        zip_ref.extractall(file_to)

for f in s_parent.rglob("*.srt"):
    if " " in f.stem:
        name = ".".join(e for e in f.stem.split(" ") if e)
        name = name.title().replace("0P.", "0p.")
        f.rename(f.with_stem(name))

infos = {}
for f in s_parent.rglob("*.srt"):
    f_stem = f.stem.lower()
    if not re.search(r"s[0-9]+\.?e[0-9]+", f_stem):
        key = re.sub(r"\.[0-9]+p\..+$", r"", f_stem)
        key = re.sub(r"[\(\)]", r"", key)
    else:
        name, s, e = re.findall(
            r"^(.+)s([0-9]+)\.?e([0-9]+)",
            f_stem,
            flags=re.IGNORECASE
        )[0]
        key = f"{name}s{int(s):02}.e{int(e):02}"
    ends = [
        k
        for k in key.split(".")
        if k and not re.search(r"^[\{\[]", k)
    ]
    if re.search(r"^[0-9]+$", ends[-1]):
        ends.pop()
    key = ".".join(ends)
    key = key.lower()
    if key not in infos:
        infos[key] = []
    infos[key].append(f)

for key, val in infos.items():
    if key in films:
        v = val[0]
        vid_file = films[key]
        srt_file = vid_file.with_suffix('.srt')
        if not srt_file.exists():
            shutil.copyfile(v, srt_file)
