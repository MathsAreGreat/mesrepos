from pathlib import Path
import re
from time import sleep
import hashlib

currentPath = "MacroDroid"
datas = {"files": [{"hash": "0", "path": "path", "name": "name"}]}


def mdfy(f: Path):
    return hashlib.md5(f.open("rb").read()).hexdigest() + str(f.stat().st_size)


paths = [
    "Android/media",
    "DualApp/WhatsApp/Media",
    "parallel_intl/0/Android/media",
    "GBWhatsApp/Media",
    "Download/GBWhatsApp ViewOnce",
]

recips = Path("Pictures/WhatsApp")
cc = 0


while cc < 2:
    try:
        for path in paths:
            for f in Path(path).rglob("*"):
                status_path = recips / "Status"
                status_path.mkdir(parents=True, exist_ok=True)
                ex = f.suffix
                if ex not in [".mp4", ".png", ".jpg"]:
                    continue
                c = str(f.parent)
                if ".Statuses" in c:
                    f.rename(status_path / f.name)
                    print(f"{f} is moved !")
                else:
                    f.rename(recips / f.name)
        for f in recips.glob("*"):
            ex = f.suffix
            if ex not in [".mp4", ".png", ".jpg"]:
                continue
            n = f.stem
            zid = ""
            dossier = ""
            if re.search(r"^Screenshot_[0-9]{8}-", n):
                dossier = "Screenshots"
                n = n.split("-")[0].split("_")[-1]
                zid = f"{n[:4]}{n[4:6]}{n[6:]}/"
            elif re.search(r"^((IMG)|(VID))-[0-9]{8}-WA[0-9]+", n):
                dossier = "WhatsApp"
                n = n.split("-")[1]
                zid = f"{n[:4]}{n[4:6]}{n[6:]}/"

            if dossier != "":
                doc = recips / f"{dossier}/{zid}"
                doc.mkdir(parents=True, exist_ok=True)
                fl = f"{mdfy(f)}{ex}"
                f.rename(doc / fl)
                print(f"{f} is moved !")
        sleep(5)
        print("=======================")
        cc = 1
    except Exception as e:
        print(e)
        print("Prov Error !")
