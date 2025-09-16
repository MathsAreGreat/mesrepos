import json
import re
from Mido.variables import egybest, monhtml
from pathlib import Path
from fnc import saison_eps, save

u = "https://www.faselhds.life/anime/%d8%a7%d9%86%d9%85%d9%8a-jidou-hanbaiki-ni-umarekawatta-ore-wa-meikyuu-wo-samayou"

# saison_eps(u)

u = "https://www.faselhds.life/anime-episodes/%d8%a7%d9%86%d9%85%d9%8a-jidou-hanbaiki-ni-umarekawatta-ore-wa-meikyuu-wo-samayou-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-3"

save(u, 1)
