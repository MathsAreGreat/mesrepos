import os
import re
from pathlib import Path
from Company import (
    HC,
    parent_path,
    use_class_by_name,
    use_direct_class_by_name,
    thumbin,
)

uns = [f.stem.split(".")[-1][1:-1].lower() for f in Path(parent_path).rglob("*mp4")]
uns = []

keys = list(os.sys.argv[1:])

hcs = [t[1:] for t in keys if t[0] == "="]

keys = [k for k in keys if k[0] != "="]

for h in hcs:
    ns, vs = HC(h).vids()
    nl = int(ns) - 1
    while True:
        keys += [e for e in set(vs) if len(e) > 10]
        if nl < 1:
            break
        _, vs = HC(h).vids(nl)
        nl -= 1
keys = [k for k in keys if k.lower() not in uns]

print(keys)

sings = [k for k in keys if re.findall(r"[a-z]", k.lower())]
nbs = [k for k in keys if k not in sings]

funs = []
if sings:
    ks = [k for k in set(sings) if k and k not in uns]
    while ks:
        print(len(ks), "items !")
        k = ks[0]
        cl = "HC"
        if re.search(r"^.+-[0-9]+", k):
            cl = "MSAV"
        elif len(k) < 10:
            cl = "SPNK"
        elif k not in funs:
            aut = HC(k).autres()
            ks += aut
            funs += aut
        use_class_by_name(cl, k)
        uns = [f.stem.split(".")[-1][1:-1] for f in Path(parent_path).rglob("*mp4")]
        ks = [k for k in set(ks) if k and k not in uns]

if nbs:
    use_direct_class_by_name(*nbs)


thumbin()
