import json
import os
from pathlib import Path
import requests

MAX = 1000000


# def run_tasks(fn, ds, nb=20):
#     def your_function(args):
#         return fn(*args)

#     with ThreadPoolExecutor(nb) as executor:
#         datas = executor.map(your_function, ds)
#     return datas


def dwn(nb):
    global MAX
    file_path = f"/home/mohamed/Documents/datas/TVMaze/Serie_{nb:06}.json"
    print(file_path, end="\r")
    if os.path.exists(file_path):
        return 0
    # if nb > MAX:
    #     return 0
    url = f'https://api.tvmaze.com/shows/{nb}?embed=episodes'
    r = requests.get(url)
    data = r.json()
    if data.get("status") and data["status"] == 429:
        # MAX = nb
        print(f"Error Serie {nb:<50}: {data["status"]}")
        return 0
    with open(file_path, "w") as fh:
        json.dump(data, fh, indent=4)
    print(f"Success Serie {nb:06}", end='\r')
    return 1


# with ThreadPoolExecutor(1) as executor:
#     datas = executor.map(dwn, list(range(1, 10001)))

pparent = Path(r"C:\Users\Mathsphile\Documents\datas\TVMaze")

datas = []
i = 1
sz = 0
for fi in pparent.glob("*json"):
    if fi.stat().st_size < 100:
        continue
    sz += fi.stat().st_size
    print(fi.name, end="\r")
    with open(fi, "r") as fl:
        data = json.load(fl)
    datas.append(data)
    if sz > 200_000_000:
        sz = 0
        with open(pparent.parent / f"comb{i}.json", "w") as fh:
            json.dump(datas, fh, indent=4)
        print(f"Comb {i} ...")
        datas = []
        i += 1

with open(pparent.parent / f"comb{i}.json", "w") as fh:
    json.dump(datas, fh, indent=4)
print(f"Comb {i} ...")
