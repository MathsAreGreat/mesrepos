from tools import *
import json
from concurrent.futures import ThreadPoolExecutor

urls = {

}
nbr = 5
s_ids = []

with open("/home/mohamed/Documents/Projects/Python/Cima4u/infos.json", "r") as e:
    nbs = json.load(e)

nbz = save_users(s_ids)


def gad(info, key="vadbam"):
    v = info.get(key)
    if v is None:
        return 0
    ep = info["EP"]
    # if int(ep) < 9:
    #     return 0
    c = info["ID"]
    ID = info["SeasonID"]
    s = nbz[ID]
    try:
        dd = globals().get(key)(v)
    except:
        return None
    if not dd:
        return None
    ref, src = dd
    title = f"{s.replace(' ', '.')}.E{ep}"
    return title, src, s, c, ref


def goo(p):
    c = 0
    while c < 10:
        d = gad(p)
        if d is not None:
            break
    if d:
        print(d)
        dwn(d)


for ids in nbs:
    print("===============================")
    ps = dlinks(ids)

    print(len(ps), "items !")
    with ThreadPoolExecutor(1) as executor:
        datas = executor.map(goo, ps)
    # for p in ps:
    #     goo(p)
