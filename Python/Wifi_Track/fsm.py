import json


with open("infos.json", "r") as fl:
    data = json.load(fl)

data = {k.upper(): v.title() for k, v in data.items()}


with open("infos.json", "w") as fl:
    json.dump(data, fl)
