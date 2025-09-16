import quopri
import json


def formater(e):
    if not e.startswith("N;"):
        return e
    _, encoded_string = e.split(":", 1)
    print(encoded_string)
    ism = quopri.decodestring(encoded_string).decode("utf-8")
    return f"N:{ism}"


with open("Contacts.vcf", "r") as e:
    data = e.read()
# BEGIN:VCARD
data = data.replace("+212", "0").replace("=\n=", "=")
datas = data.split("END:VCARD")
arr = []
for dt in datas:
    info = [
        formater(e).split(":", 1)
        for e in dt.split("\n")
        if e.strip() and "photo" not in e.lower()
    ]
    info = [e for e in info if len(e) == 2]
    infos = {}
    for k, v in info:
        if k.startswith(("FN", "BEGIN", "VERSION")):
            continue
        k = k.split(";", 1)[0]
        if k not in infos:
            infos[k] = []
        if v not in infos[k]:
            infos[k].append(v)
    arr.append({k: v if len(v) > 1 else v[0] for k, v in infos.items()})

with open("contacts.json", "w") as e:
    json.dump(arr, e)
