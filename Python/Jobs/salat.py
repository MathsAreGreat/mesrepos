from datetime import datetime, timedelta
import json
from pathlib import Path
from Mido.variables import monhtml
import notify2

days = [None, "08:40", None, "12:30", "08:40", "13:40", "08:40"]

soup = monhtml(
    "https://app.muslimpro.com/prayer-times/morocco/taroudant?lat=30.4727126&lng=-8.8748765&alt=236.82470703125&country_code=MA"
)


def send_notification(intial, title, temp):
    try:
        notify2.init(intial)
        img = f"/home/mohamed/Pictures/Notications/salat.png"
        message = f"10 minutes to {title} [{temp}]"
        n = notify2.Notification(title, message, img)
        n.set_timeout(1000)
        n.show()
    except Exception as err:
        print(err)


salawat = soup.select_one("#prayer-times-jsonld").text
dt = datetime.now() + timedelta(minutes=10)
pd = "/home/mohamed/Documents/datas/Backups"
db = dt.strftime("%H:%M")


info = json.loads(salawat)

intial = info["name"]

salats = [
    (e["startDate"].split("T")[-1].rsplit(":", 2)[0], e["name"])
    for e in info["itemListElement"]
]

infos = {t: s for t, s in salats if t >= db and not Path(f"{pd}/{t}").exists()}

print(db, infos)

if db in infos:
    send_notification(intial, infos[db], db)
    Path(f"{pd}/{db}").touch()
