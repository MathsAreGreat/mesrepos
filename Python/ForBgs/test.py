from pathlib import Path
import json
import re
from Company import HC, SPNK
import requests

from Mido.variables import run_tasks

pr = Path("/home/mohamed/.Kindas")
pu = pr / "Files"
pi = pr / "IMGs"

pi.mkdir(parents=True, exist_ok=True)

keys = []
for f in pu.glob("*json"):
    with f.open("r") as fl:
        data = json.load(fl)
    actor = data.get("actress")
    if not actor:
        continue
    # if "Ozawa" not in actor:
    #     continue
    print((f.stem, ":", data))
