import requests
import json
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": "https://cimaa4u.show/"
}

# datas = {}
# process = True
# i = 1
# owner = "ahaspoorts"
# while process:
#     u = f"https://api.dailymotion.com/user/{owner}/videos?limit=100&page={i}"
#     r = requests.get(u)
#     info = r.json()
#     print("Page", i)
#     process = info["has_more"]
#     for dt in info["list"]:
#         datas[dt["id"]] = dt["title"]
#     i += 1


# with open(f"{owner}.json", "w") as fl:
#     json.dump(datas, fl)

u = "https://ok.ru/group/70000034451327/video"
r = requests.get(u)
arr = re.findall(r"video/[0-9]+", r.text)
print(set(arr))
