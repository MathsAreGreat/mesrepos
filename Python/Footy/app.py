from Besites.variables import multiple, fetch
import json

links = []

for i in range(1, 6):
    print("> Page", i)
    multiple(i)


keys = fetch()

with open("infos.json", "w") as f:
    json.dump(keys, f, indent=4)
