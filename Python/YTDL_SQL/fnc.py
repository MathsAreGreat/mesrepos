import re
from concurrent.futures import ThreadPoolExecutor
import json
import os

d_path = "Videos/%(id)s.%(ext)s"
s_path = "Videos/Files/%(title)s/%(upload_date)s_%(section_title)s (%(id)s).%(ext)s"

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

DOM = "https://www.youtube.com"

fs = {
    "أغنية بداية": "أغاني البداية",
    "اغنية بداية": "أغاني البداية",
    "مبقتش": "Mesh 7eml",
    "فيلملوخية": "Filmolokhia",
    "عدامات في الكويت": "سلسلة كتاب الإعدامات في الكويت",
    "جت علينا": "Gat3alena",
    " أزرق": "بودكاست أزرق",
    " وجدان": "بودكاست وجدان",
    " هدوء": "بودكاست هدوء",
    " جذور": "بودكاست جذور",
    "بيت الوجود": "بودكاست بيت الوجود",
    "شاما": "Chaama",
    "خر الليل": "آخر الليل",
    "منقوطة": "فاصلة منقوطة",
    "سلام عادل": "بصوت إسلام عادل",
    "شيخ الشعراوي": "الشيخ محمد متولي الشعرواي",
    "عارف حجّاوي": "بودكاست مع عارف حجّاوي",
    "عارف حجاوي": "بودكاست مع عارف حجّاوي",
    "بودكاست مشربية": "مشربية بودكاست",
    "بودكاست تنوين": "تنوين بودكاست",
    "الاسبتالية": "الإسبتالية",
    "الكرة الثانية": "الكورة الثانية",
}

ds = [
    "D33pSoul",
    "Eljoee",
    "Faylasuf",
    "Zamane",
    "Recham",
    "Nordo",
    "بودكاست مما قرأت",
    "Ta Ha",
    "بودكاست استشارة",
    "Carmen Tockmaji",
    "Wardi & Friends",
    "Alaa Wardi",
    "نظام التفاهة",
    "تأملات",
    "الإسبتالية",
    "فيودور دوستويفسكي",
    "مصطفى محمود",
    "شيرلوك هولمز",
    "أحمد خالد توفيق",
    "شوربة دجاج للحياة",
    "حول العالم في ٢٠٠ يوم",
    "أجاثا كريستي",
    "انهيار الحضارة",
    "في الحضارة",
    "مع بندق",
    "مع تميم",
    "ذات مرة",
    "علم كرة القدم",
    "محدش طلب رأيك",
    "مواهب ضائعة",
    "الكورة الثانية",
    "مراتب",
    "توب 5",
    "سافاري",
    "بيت الأسرار",
    "رجل يعرف كل الأسرار",
    "العادات الذرية",
    "Shorts",
    "Chaama",
    "لؤي یحكي",
    "صورة تروى",
    "شرح فيلم",
    "نجيب محفوظ",
    "روايات مسموعة",
    "كتاب صوتي",
    "Zamane",
    "بودكاست قبل الغروب",
    "بودكاست سهالات",
    "بودكاست مهارات",
    "بودكاست أسمار",
    "بودكاست الغرفة",
    "بودكاست كنبة السبت",
    "مع الطنطاوي",
    "بودكاست نقرة",
    "ابتهالات رمضان",
    "بودكاست سيَر",
    "مشربية بودكاست",
    "أصداء بودكاست",
    "تنوين بودكاست",
    "بودكاست نجاة",
    "برشام",
    "الدحيح",
    "سؤال وجواب",
    "عاركني",
]

cs = {e: e.title() for e in ds}
cs.update(fs)

users = {
    "AJplussaha": "AJplus Saha",
    "TheYahyaAzzam": "Yaya Azzam",
    "MicsPodcast": "Mics Podcasts",
    "anaalaraby": "Mohamed Saadani",
    "9li9": "عبدالرحمن مسعد",
    "abdulrahmanmosad9736": "عبدالرحمن مسعد",
    "NewMedia_Life": "الدحيح",
    "m3kamele7trami": "Mohamed Abd Elati",
    "tasgeelpodcast": "Tasgeel Podcast",
    "EslamAdel": "Eslam Adel",
    "FahmyProductions": "Fahmy Productions",
    "user-yj5vt8ki7u": "طحالب",
    "Tahalip": "طحالب",
    "-haidurant391": "haidurant",
    "janazeermedia2": "طحالب",
    "Filmolokhia": "Mohamed Goely",
}

reverses = {"الدحيح": "New Media Academy Life", "haidurant": "لفهم التاريخ"}

keys = [
    "title",
    "channel_id",
    "duration",
    "subtitles",
    "chapters",
    "uploader",
    "uploader_id",
    "upload_date",
]


def thumbnaudio(nbr):
    q = "bestaudio"
    dp = "Audios/%(id)s.%(ext)s"
    url = nbr
    if not nbr.startswith("PL"):
        url = f"{DOM}/watch?v={nbr}"
    sub = "--write-sub --sub-langs all,-live_chat --ignore-errors"
    cmd = f'yt-dlp -f "{q}" "{url}" -o "{dp}" {sub}'
    os.system(cmd)
    print(upclear * 10, end="")


def viding(nbr, dp):
    q = "bestaudio+bestvideo"
    url = nbr
    if not nbr.startswith("PL"):
        url = f"{DOM}/watch?v={nbr}"
    sub = "--write-sub --sub-langs ar,fr,en,-live_chat --ignore-errors"
    cmd = f'yt-dlp -f "{q}" "{url}" -o "{dp}" {sub}'
    os.system(cmd)
    print(upclear * 10, end="")


def subtitre(nbr, dp):
    url = f"{DOM}/watch?v={nbr}"
    sub = "--write-sub --sub-langs ar,fr,en,-live_chat --ignore-errors"
    cmd = f'yt-dlp --skip-download "{url}" -o "{dp}" {sub}'
    os.system(cmd)
    print(upclear * 10, end="")


def gad(l):
    data = json.loads(l)
    if data["title"] == "[Private video]":
        return None
    keys = {"id", "playlist_id", "playlist_title"}
    info = {k: v for k, v in data.items() if k in keys}
    for c, v in cs.items():
        if c.lower() in data["title"].lower().replace("_", " "):
            info["playlist_title"] = v
            break
    return info


def save(l):
    data = gad(l)
    if not data:
        return 0
    c = data["id"]
    json_file = f"Files/{c}.json"
    if os.path.exists(json_file):
        return 0
    dd = (f"=={c}", 1, "")
    datas = channelize(dd)
    if not datas:
        return 0
    infos = {k: datas[k] for k in keys if k in datas}
    infos.update(data)
    tb = infos["subtitles"]
    if tb:
        k = "live_chat"
        if k in tb:
            del tb[k]
        for key, val in tb.items():
            tb[key] = val[-1]["url"]
        infos["subtitles"] = tb
    k = "id"
    if k in infos:
        del infos[k]

    with open(json_file, "w") as e:
        json.dump(infos, e, indent=2)
    return 1


def channelize(dd):
    c, mx, *fs = dd
    if mx < 0:
        return 0
    json_file = f"Files/{c}.json"
    if os.path.exists(json_file):
        return {}
    r = "rjwwx"
    if not fs:
        f = ""
    elif len(fs) < 2:
        f = fs[0]
        if f.startswith("+="):
            f = ""
            r = fs[0][2:]
    else:
        f = "|".join(f"({e})" for e in fs if not e.startswith("+="))
        r = "|".join(f"({e[2:]})" for e in fs if e.startswith("+="))
    cnt = 1
    txt_file = f"Files/{c}.txt"
    if not os.path.exists(txt_file):
        dd = f"{DOM}/@{c}/videos"
        if c.startswith("UC"):
            dd = f"{DOM}/channel/{c}/videos"
        elif c.startswith("PL"):
            dd = f"{DOM}/playlist?list={c}"
        elif c.startswith("=="):
            c = c[2:]
            dd = f"{DOM}/watch?v={c}"
            cnt = 0
        print("Loading", c, "!")
        cmd = f'yt-dlp "{dd}" --flat-playlist --dump-json'
        if mx:
            cmd += f' --playlist-end "{mx}" '
        cmd += f' --match-title "{f}"'
        cmd += f' --reject-title "{r}"'
        cmd += f" > {txt_file}"
        os.system(cmd)
        print("Loaded", c, "!")
    if cnt:
        with open(txt_file, "r") as e:
            lines = [e.strip() for e in e.readlines() if e.strip()]
        os.remove(txt_file)
        lines = list(set(lines))
        with ThreadPoolExecutor() as executor:
            executor.map(save, lines)
        print(">", c)
        return {}
    with open(txt_file, "r") as e:
        lines = e.read()
    if not lines:
        return {}
    os.remove(txt_file)
    datas = json.loads(lines)
    print(upclear * 10, end="")
    return datas


def stablize(ds):
    for f in os.listdir("Files"):
        fn = f"Files/{f}"
        if not f.endswith(".json"):
            os.remove(fn)
            continue
        with open(fn, "r", encoding="utf-8") as e:
            data = json.load(e)
        uid = data.get("uploader_id")
        if uid:
            uid = uid[1:]
            ar = uid
            if ar in users:
                print(ar, "=>", users[ar])
                ar = users[ar]
                data["uploader"] = ar
            data["title"] = " ".join(e for e in data["title"].split(" ") if e)
            stop = 0
            pls = ds.get(uid)
            pt = None
            if pls:
                pt = pls[-1].split("|")[-1]
                for p in pls[:-1]:
                    pz = p.split("|")
                    for z in pz:
                        v = z.replace("*", ".+")
                        if re.search(rf"{v}", data["title"]):
                            pt = pz[-1].strip().replace("*", " ")
                            stop = 1
                            break
                    if stop:
                        break
            if ar in reverses:
                pt = reverses[ar]
            if pt:
                print("* PL :", pt)
                data["playlist_title"] = pt
            with open(fn, "w") as e:
                json.dump(data, e)
            print(upclear * 10, end="")
