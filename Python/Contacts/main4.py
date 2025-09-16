import json
import base64



def foto(k):
    try:
        with open(f"/home/mohamed/Pictures/Massar/{k}.png", "rb") as image_file:
            image_binary_data = image_file.read()
        base64_encoded = base64.b64encode(image_binary_data)
        return base64_encoded.decode("utf-8")
    except:
        return None


with open("contacts.json", "r") as e:
    arr = json.load(e)

with open("eleves.json", "r") as e:
    els = json.load(e)


contacts = {}
for info in arr:
    if not info:
        continue
    name = info["N"]
    tels = info["TEL"]
    del info["TEL"]
    if isinstance(tels, list):
        for i, t in enumerate(tels, start=1):
            if t not in contacts:
                contacts[t] = []
            contacts[t].append(name)
    else:
        if tels not in contacts:
            contacts[tels] = []
        contacts[tels].append(name)

print({k: v for k, v in contacts.items() if len(v) > 1})
