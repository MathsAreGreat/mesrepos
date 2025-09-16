import json

with open("sites", "r") as f:
    datas = [e.strip() for e in f.read().split("=") if e.strip()]

with open("infos.json", "r") as e:
    animes = json.load(e)

for block in datas:
    item = {}
    for e in block.split("\n"):
        if "/" not in e:
            continue
        k = e.split("/")[2].split(".")[-2]
        item[k] = e.strip()
    if item in animes:
        continue
    item = {k: item[k] for k in sorted(item)}
    animes.append(item)
    print(item)
    print("============")

with open("infos.json", "w") as e:
    json.dump(animes, e, indent=4)
