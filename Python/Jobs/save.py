import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from final import monfile, uns

directory = Path("/home/mohamed/Documents/.Socials")
dirc = Path("/home/mohamed/Documents/.Socials")


datas = Path("/home/mohamed/Documents/Projets/Python/Facebook/Datas")
vids = Path("/home/mohamed/Documents/Projets/Python/Facebook/Vids")

files = [f for f in datas.glob("*json") if f.stem not in uns]
if len(files):
    print(len(files), "here !")
    with ThreadPoolExecutor(10) as executor:
        executor.map(monfile, files)

    datas = dirc / "Facebook"
    pvids = dirc / "FBs"
    files = [(e.stem,) for e in Path("Vids").glob("*")]
    files += [
        [e for e in f.stem.split("_") if len(e) > 10]
        for f in datas.rglob("*.*")
        if f.is_file()
    ]
    files += [
        [e for e in f.stem.split("_") if len(e) > 10]
        for f in pvids.rglob("*.*")
        if f.is_file()
    ]

    for f in files:
        if not f:
            continue
        f = f[0]
        fn = Path("/home/mohamed/Documents/Projets/Python/Facebook/Datas") / f"{f}.json"
        if fn.exists():
            fn.unlink()
            print(":>", fn)
        fn = vids / f"{f}.json"
        if fn.exists():
            fn.unlink()
            print(":>", fn)
        doc = dirc / "Vids"
        doc.mkdir(parents=True, exist_ok=True)
        fn = doc / f"{f}_vid.jpg"
        fn.touch()
    print(":: kmlt hna !!")


infos = {}
parent = Path("/home/mohamed/Documents/Stuff/Jups")
fbs = Path("/home/mohamed/Documents/.Socials/FBs")
for f in parent.rglob("*json"):
    with open(f, "r") as el:
        data = json.load(el)
    for ID in data["IDs"]:
        k = ID.replace("v", "")
        infos[k] = data["username"]

for f in fbs.glob("NoUser/*.*"):
    k = f.stem.split("_")[2]
    if k in infos:
        doc = fbs / infos[k]
        doc.mkdir(parents=True, exist_ok=True)
        fn = doc / f.name
        f.rename(fn)


doc = Path("/home/mohamed/Downloads")
jp = Path("/home/mohamed/Documents/Stuff/Jups")
jp.mkdir(parents=True, exist_ok=True)
for f in doc.glob("dis*json"):
    with open(f, "r") as fl:
        data = json.load(fl)
    idm = data["ID"]
    ids = data["savedData"]
    pseudo = data["pseudo"]
    username = data["username"].replace(" ", ".")
    fn = jp / f"{idm}.json"
    data = {"username": username, "pseudo": pseudo, "IDs": ids}
    if fn.exists():
        with open(fn, "r") as fl:
            data = json.load(fl)
        print(len(data["IDs"]))
        print(len(ids))
        ids += data["IDs"]
        data["username"] = username
        data["pseudo"] = pseudo
        data["IDs"] = sorted(set(ids))
    print(len(data["IDs"]))
    with open(fn, "w") as fl:
        json.dump(data, fl)
    f.unlink()
