from numpy import base_repr
import os
import re
agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
# agent = "spis16t3 bot 1.0"
referrer = 'https://play-1.reyada-365.com/'
referrer = 'https://live83.yalla-shoot-tv.biz/chtv/ch1.php'


def decode_string(p, a, c, k, e, d):
    def e_func(c):
        return (e_func(c // a) if c >= a else "") + (
            chr(c + 29) if (c := c % a) > 35 else base_repr(c, 36).lower()
        )

    while c > 0:
        c -= 1
        d[e_func(c)] = k[c] or e_func(c)

    p = re.sub(r"\b\w+\b", lambda m: d.get(m.group(0), ""), p)

    return p


def urlize(tt):
    tt = tt.replace("\\'", "<&>")
    datas = tt.split("'")
    ind = datas.index(".split(")
    exp, tnb, wst = datas[ind - 3: ind]
    tnb = [int(e) for e in tnb.split(",") if e.strip()]
    r = decode_string(
        exp.replace("<&>", "'"), *
        tnb, wst.replace("<&>", "'").split("|"), 0, {}
    )
    return re.findall(r"http[^\"']+m3u[^\"']+", r)[0]


# url = "https://gvy5m18ysvp67j.dynamicsupply.net/embed/jpe9zodoh"
# sess = requests.session()
# sess.headers = {
#     "referer": referrer,
#     "User-Agent": agent
# }
# r = sess.get(url)

# tt = r.text
# print(len(tt))
# referrer = url
# url = urlize(tt)

url = "https://gfbdtp8er926573sjzywha.cdnexpertise.net:8443/hls/jpe9zodoh.m3u8?s=H_EklrTxNeyc0EqObx5Abg&e=1730609917"
url = "https://gfbdtp8er926573sjzywha.cdnexpertise.net:8443/hls/jpe9zodoh.m3u8?s=ixe5ZRlbk-Ssqk4xa30kWw&e=1730610042"
referrer = "https://l7e5m6eehdlwlp.dynamicsupply.net/"
print(url)
settings = f'--http-referrer="{referrer}" --http-user-agent="{agent}"'
cmd = f"""vlc "{url}" {settings}"""
os.system(cmd)
