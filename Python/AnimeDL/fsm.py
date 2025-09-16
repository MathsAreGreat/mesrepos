import json
import re
import shutil
from Besites.mp4upload import goo as mgoo
from Besites.okru import goo as kgoo
from Besites.videa import goo as vgoo
from Besites.daily import goo as dgoo
from pathlib import Path

with open("segs.json", "r") as e:
    segs = json.load(e)

Path("/home/mohamed/Documents/datas/AnimeDL/vides").mkdir(exist_ok=True, parents=True)

NBS = 1
while NBS > 0:
    uniques = [
        re.sub(r"\.END$", r"", f.stem)
        for f in Path("Library/MixAnimes").rglob("*.mp4")
    ]

    uniques += [
        re.sub(r"\.END$", r"", f.stem)
        for f in Path("/home/mohamed/Downloads/Library/MixAnimes").rglob("*.mp4")
    ]

    # uniques += [
    #     f.name
    #     for f in Path(
    #         "/home/mohamed/Documents/datas/AnimeDL/vides").rglob("*")
    # ]

    oks = []
    mps = []
    dms = []
    vds = []
    NBS = 0
    for k, v in segs.items():
        if k in uniques or not v:
            continue
        ks, ep = k.rsplit("-", 1)
        name = ks.replace("-", ".").title()
        if f"{name}.E{ep}" in uniques:
            Path(
                f"/home/mohamed/Documents/datas/AnimeDL/vides/{k}").touch()
            continue
        print(f"> {name}.E{ep}")
        key, e = max(v.items(), key=lambda e: e[1]["size"])
        if e["site"] == "okru":
            oks.append((key, f"{name}.E{ep}"))
        elif e["site"] == "dailymotion":
            dms.append((key, f"{name}.E{ep}"))
        elif e["site"] == "mp4upload":
            mps.append((name, ep, key))
        elif e["site"] == "videa":
            vds.append((name, ep, key))

    while dms:
        NBS += 1
        dgoo(dms[:1])
        dms = dms[1:]
    while oks:
        NBS += 1
        kgoo(oks[:1])
        oks = oks[1:]
    if mps:
        NBS += 1
        mgoo(mps)
    if vds:
        NBS += 1
        vgoo(vds)

    nb = 1

    while nb:
        nb = 0
        for doc in Path("Library/MixAnimes").rglob("*"):
            if doc.is_file() and doc.suffix == ".mp4":
                parts = doc.parts
                fn = Path("/home/mohamed/Downloads", *parts)
                if fn.exists():
                    fn.unlink()
                fn.parent.mkdir(exist_ok=True, parents=True)
                doc.rename(fn)
                nb += 1
            else:
                try:
                    doc.rmdir()
                    nb += 1
                    print(doc)
                except:
                    continue

shutil.rmtree("datas", ignore_errors=True)
