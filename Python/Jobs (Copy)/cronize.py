import os
import json
pp = "/home/mohamed/Documents/datas/Crons"

try:
    with open('scripts.json', "r") as e:
        infos = json.load(e)
except:
    infos = {}

for f in os.listdir():
    try:
        name, ex = f.rsplit('.', 1)
        if ex == "py" and name not in infos:
            infos[name] = "* * * * *"
    except:
        pass

with open('scripts.json', "w") as e:
    json.dump(infos, e, indent=2)

os.chdir(pp)

fn = "schedule.cr"
datas = []
for name, often in infos.items():
    if not often:
        continue
    ptn = "/home/mohamed/miniconda3/envs/moha/bin/python"
    script = f"/home/mohamed/Documents/Projects/Python/Jobs/{name}.py"
    newline = f"{often} {ptn} {script}"
    datas.append(newline)
    if often != "@reboot" and not often.startswith('*'):
        often = "@reboot"
        newline = f"{often} {ptn} {script}"
        datas.append(newline)

newline = ""
datas.append(newline)
text = "\n".join(datas)
with open(fn, "w") as e:
    e.write(text)
os.system('crontab schedule.cr')
