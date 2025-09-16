import hashlib
import json
from pathlib import Path


directory = Path("/home/mohamed/Downloads/Files/Pdfs/AlloSchool")
p = directory / "files_md5.json"
try:
    with open(p, "r") as e:
        files_md5 = json.load(e)
    files_md5 = {
        k: v
        for k, v in files_md5.items()
        if Path(f"/home/mohamed/Downloads/Files/Pdfs/AlloSchool/{v[0]}/{v[1]}").exists()
    }
except:
    files_md5 = {}

existed_files = [directory / p / n for p, n in files_md5.values()]

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear


def md5ify(file_path, nb):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    file_hash = str(hash_md5.hexdigest())
    print(f"{upclear}> {nb:05} | {file_path.name} : {file_hash}")
    return file_hash, file_path.parent.name, file_path.name


def find_duplicate(files_md5):
    directory = Path("/home/mohamed/Downloads/Files/Pdfs/AlloSchool")
    files = [f for f in directory.rglob("*pdf") if f not in existed_files]
    hash_datas = directory / "files_md5.json"
    print(len(files), "files !")
    print()
    for i, f in enumerate(files, start=1):
        if f in existed_files:
            print(f"{upclear}> {i:05} {f.name}")
            continue
        data = md5ify(f, i)
        if not data:
            continue
        file_hash, p, name = data
        if file_hash not in files_md5:
            files_md5[file_hash] = [p, name]
            with open(hash_datas, "w") as e:
                json.dump(files_md5, e)
        elif f.name != files_md5[file_hash][-1]:
            doc = Path("/home/mohamed/Documents/datas/Duplicates") / p
            doc.mkdir(parents=True, exist_ok=True)
            f.rename(doc / name)


if __name__ == "__main__":
    find_duplicate(files_md5)
    doc = Path("/home/mohamed/Documents/Projects/PYTHON/AlloSchool/vides")
    for f in Path("/home/mohamed/Documents/datas/Duplicates").rglob("*pdf"):
        k = f.stem.split("-")[-1]
        fn = doc / k
        fn.touch()
    uns = [f.name for f in doc.rglob("*")]
    for f in Path("/home/mohamed/Documents/datas/Duplicates").rglob("*pdf"):
        k = f.stem.split("-")[-1]
        if k in uns:
            f.unlink()
            print(k)
    nb = 1
    while nb:
        nb = 0
        for f in Path("/home/mohamed/Downloads/Files/Pdfs/AlloSchool").glob("*"):
            try:
                f.rmdir()
                nb += 1
            except Exception as err:
                print(err)
        for f in Path("/home/mohamed/Documents/datas/Duplicates").glob("*"):
            try:
                f.rmdir()
                nb += 1
            except Exception as err:
                print(err)
