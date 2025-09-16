import tools
import json

urls = []
nbr = 5
s_ids = []

with open("/home/mohamed/Documents/Projects/Python/Cima4u/infos.json", "r") as e:
    nbs = json.load(e)

nbz = tools.save_users(s_ids, nbs)

for ids in nbs:
    print("===============================")
    ps = tools.dlinks(ids)

    def gad(info):
        v = info.get("vidpro")
        if v is None:
            return None
        print("**", v)
        ID = info["SeasonID"]
        s = nbz[ID]
        res = tools.vidpro(v)
        if not res:
            return None
        _, src = res
        ep = info["EP"]
        title = f"{s.replace(' ', '.')}.E{ep}"
        return title, src

    print(len(ps), "items !")
    print()
    print()
    for info in ps:
        c = 0
        while c < 10:
            v = gad(info)
            if v:
                break
            c += 1
        print(v)
