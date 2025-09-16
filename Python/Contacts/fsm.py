import base64

with open("/home/mohamed/Pictures/32082.jpg", "rb") as image_file:
    image_binary_data = image_file.read()
base64_encoded = base64.b64encode(image_binary_data)
base64_string = base64_encoded.decode("utf-8")

info = {
    "first": "Mohamed",
    "last": "OUALIL",
    "note": "JB382242",
    "bday": "1987-01-13",
    "org": "Ziraoui",
    "department": "Maths",
    "title": "Professeur",
    "base64_string": base64_string,
    "tels": {"CELL": "0636534456", "HOME": "0636534456", "Orange": "0693403496"},
    "adrs": {"HOME": ";;Sidi Bel Kass;Taroudant;Souss;;Morocco"},
    "emails": {
        "Perso": "simoualil@gmail.com",
        "Professional": "mathsphile@gmail.com",
    },
}


def datafy(
    first,
    last,
    base64_string=None,
    note="",
    bday="",
    org="",
    department="",
    title="",
    tels={},
    emails={},
    adrs={},
    urls=[],
):
    data = f"""
BEGIN:VCARD
VERSION:2.1
N:{last};{first};;;
NOTE:{note}
BDAY:-{bday}
ORG:{org};{department}
TITLE:{title}
"""
    if base64_string:
        data += f"PHOTO;ENCODING=BASE64;JPEG:{base64_string}\n"
    for k, v in tels.items():
        data += f"TEL;{k}:{v}\n"

    for k, v in emails.items():
        data += f"EMAIL;{k}:{v}\n"

    for k, v in adrs.items():
        data += f"ADR;{k}:{v}\n"

    for k in urls:
        data += f"URL:{k}\n"
    data += "END:VCARD"
    return data


data = datafy(**info)

with open(f"{info['note']}.vcf", "w") as e:
    e.write(data)
