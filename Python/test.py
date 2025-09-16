from pathlib import Path

men = "from SMido."
ila = "from Mido."

parent_path = Path("/home/mohamed/Documents/Projects/Python")

datas = []
for doc in parent_path.rglob("*.py"):
    with doc.open("r") as fl:
        data = fl.read()
    if men not in data or "ila = " in data:
        continue
    data = data.replace(men, ila)
    print(doc.name)
    with doc.open("w") as fl:
        fl.write(data)

for doc in parent_path.glob("*"):
    if not doc.is_dir():
        continue
    sz = 0
    for f in doc.rglob("*"):
        if not f.is_file():
            continue
        sz += f.stat().st_size
    datas.append((sz, doc.name))

for s, n in sorted(datas, reverse=True):
    if s < 1000000:
        continue
    print("::", n, f": {s / 1000000:.2f} MB")
