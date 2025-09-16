import json
import base64


def foto(k):
    try:
        with open(
            f"/home/mohamed/Pictures/Massar/converts/{k}.png", "rb"
        ) as image_file:
            image_binary_data = image_file.read()
        base64_encoded = base64.b64encode(image_binary_data)
        return base64_encoded.decode("utf-8")
    except:
        return None


with open("contacts.json", "r") as e:
    arr = json.load(e)

with open("eleves.json", "r") as e:
    els = json.load(e)


residus = []
contacts = []
for info in arr:
    if not info:
        continue
    if "NOTE" not in info:
        residus.append(info)
        continue
    cle = info["NOTE"]
    tels = info["TEL"]
    del info["TEL"]
    if isinstance(tels, list):
        for i, t in enumerate(tels, start=1):
            info[f"TEL;CELL{i}"] = t
    else:
        info["TEL;CELL"] = tels
    if cle in els:
        # base64_string = foto(cle)
        # if base64_string:
        #     info["PHOTO;ENCODING=BASE64;GIF"] = base64_string
        v = els[cle]
        info["NOTE"] = cle
        info["N"] = f"{v['nom']};{v['prenom']};;;"
        info["TITLE"] = "Student"
        info["ORG"] = f"{v['section_name']};2023-2024"
        info["BDAY"] = f"-{v['birthday']}"
        del els[cle]
    contacts.append(info)

for k, v in els.items():
    info = {}
    # base64_string = foto(k)
    # if base64_string:
    #     info["PHOTO;ENCODING=BASE64;GIF"] = base64_string
    info["NOTE"] = k
    info["TEL;CELL"] = "0000"
    info["N"] = f"{v['nom']};{v['prenom']};;;"
    info["TITLE"] = "Student"
    info["ORG"] = f"{v['section_name']};2023-2024"
    info["BDAY"] = f"-{v['birthday']}"
    contacts.append(info)

vcard = ["\n".join(f"{k}:{v}" for k, v in info.items()) for info in contacts]
vcard = "\n".join(f"BEGIN:VCARD\nVERSION:2.1\n{info}\nEND:VCARD" for info in vcard)
with open("Students_Phones.vcf", "w") as e:
    e.write(vcard)

vcard = ""
for res in residus:
    vcard += "\nBEGIN:VCARD"
    for k, tels in res.items():
        if isinstance(tels, list):
            for i, t in enumerate(tels, start=1):
                vcard += f"\n{k};CELL{i}:{t}"
        else:
            vcard += f"\n{k}:{tels}"
    vcard += "\nEND:VCARD"
with open("Residus_Phones.vcf", "w") as e:
    e.write(vcard)
with open("Residus.json", "w") as e:
    json.dump(residus, e)
