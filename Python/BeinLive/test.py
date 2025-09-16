import json


with open("chs.json", "r") as f:
    chz = json.load(f)

for i in range(9):
    chz[f"tsn{i+1}"] = f"premium{111+i}"
    chz[f"bein{i+1}"] = f"premium{91+i}"
    chz[f"beinf{i+1}"] = f"primabeinsport{i+1}france247"
    chz[f"ttsn{i+1}"] = f"eplayerTSN_{i+1}_HD"
    chz[f"fox{i+1}"] = f"primafox{i+1}"

chz["pfox1"] = "premium39"

ks = [
    "skyf1",
    "bbc",
    "rtl",
    "zdf",
    "espn",
    "tnt",
    "abc",
    "yes",
    "lequipetv",
    "fussball1",
    "fox"
]
for k in ks:
    chz[k] = f"prima{k}"

chz["zdf1"] = "premium9"
chz["zdf2"] = "premium10"
chz["euro1"] = "premium41"
chz["euro2"] = "premium42"

chz["bein1x"] = "premium100"

chz["bein1fr"] = "premium116"
chz["bein2fr"] = "premium117"
chz["bein3fr"] = "premium118"

chz["bein1tr"] = "premium62"
chz["bein2tr"] = "premium63"
chz["bein3tr"] = "premium64"
chz["bein4tr"] = "premium67"

chz["rmc1"] = "premium119"
chz["rmc2"] = "premium120"
chz["rmc3"] = "premium121"

chz["bbc1"] = "primabbc2live"
chz["rai1"] = "primaraiuno"
chz["beinaus"] = "premium61"

with open("chz.json", 'w') as f:
    json.dump({k: chz[k] for k in sorted(chz)}, f, indent=4)
