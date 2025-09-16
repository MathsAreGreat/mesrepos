import json
from pathlib import Path
from Mido.variables import download_m3u8_with_aria2c

for f in Path("/home/mohamed/Downloads/Library/Anime").rglob("*.mp4"):
    print(f.stem)
    Path(f"Backups/{f.stem}").touch()


DOWN = Path("/home/mohamed/Downloads/Library")
site = "https://www.dailymotion.com"

with Path("/home/mohamed/Documents/datas/Daily/Dailymotion/naruhinamov.json").open(
    "r"
) as fl:
    datas = json.load(fl)


with Path("/home/mohamed/Documents/datas/Daily/Dailymotion/witpaly_tv.json").open(
    "r"
) as fl:
    datas |= json.load(fl)


with Path("/home/mohamed/Documents/datas/Daily/dailymotion.json").open("r") as fl:
    datas_infos = json.load(fl)

items = []
for k, v in datas.items():
    if v["created_time"] < "2020":
        continue
    c = v["title"].lower().split(" ")[1]
    if not datas_infos.get(c):
        continue
    dd = k, v["title"], datas_infos[c]
    items.append(dd)

items = sorted(items, key=lambda e: e[1].lower())

dazt = []

keys = [
    "MZNM",
]

for k, t, s in items:
    for key in keys:
        if f"] {key} EP" not in t:
            continue
        name = ".".join(s.split(" ") + t.split(" ")[2:-1])
        if name in dazt or Path(f"Backups/{name}").exists():
            continue
        dazt.append(name)
        print(name)
        file_file = DOWN / f"Anime/{s}/{name}.mp4"
        if not file_file.exists():
            url = f"{site}/video/{k}"
            if download_m3u8_with_aria2c(url, file_file, site):
                break


for f in Path("/home/mohamed/Downloads/Library/Anime").rglob("*.mp4"):
    Path(f"Backups/{f.stem}").touch()

# with Path("/home/mohamed/Documents/datas/Daily/okru.json").open("r") as fl:
#     datas = json.load(fl)

# # ==================================================================

# items = []
# for k, v in datas.items():
#     c = v.lower().split(" ")[1]
#     if not datas_infos.get(c):
#         continue
#     dd = k, v, datas_infos[c]
#     items.append(dd)

# items = sorted(items, key=lambda e: e[1].lower())

# dazt = []

# site = "https://www.ok.ru"

# for k, t, s in items:
#     for key in keys:
#         if f"] {key} EP" not in t:
#             continue
#         name = ".".join(s.split(" ") + t.split(" ")[2:-1])
#         if name in dazt:
#             continue
#         dazt.append(name)
#         print(name)
#         file_file = DOWN / f"Anime/{s}/{name}.mp4"
#         if not file_file.exists():
#             url = f"{site}/video/{k}"
#             if download_m3u8_with_aria2c(url, file_file, site):
#                 break
