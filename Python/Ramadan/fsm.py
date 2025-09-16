from datetime import datetime, timedelta
from Mido.variables import monhtml
import notify2

days = [None, "08:40", None, "12:30", "08:40", "13:40", "08:40"]

soup = monhtml(
    "https://prayer-times.muslimpro.com/fr/Horaires-prieres-adhan-Taroudant-Morocco-2529649"
)


def send_notification(title, temp):
    notify2.init("Salat Time")
    img = f"/home/mohamed/Pictures/Notications/salat.png"
    message = f"5 minutes to {title} [{temp}]"
    n = notify2.Notification(title, message, img)
    n.set_timeout(1000)
    n.show()


def gor(t):
    h, m = t.split(":")
    ms = int(h) * 60 + int(m) - 10
    h, m = divmod(ms, 60)
    return f"{h:02}:{m:02}"


salawat = [el.text for el in soup.select(".waktu-solat")]
times = [el.text for el in soup.select(".jam-solat")]
dt = datetime.now() + timedelta(minutes=10)
db = dt.strftime("%H:%M")

infos = {t: s for t, s in zip(times, salawat) if t >= db}


if db in infos:
    send_notification(infos[db], db)
