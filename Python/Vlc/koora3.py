import os
import requests
import re
from urllib.parse import unquote


agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

sess = requests.session()
referrer = "https://al-aqsanews.com/"
sess.headers = {
    "user-agent": agent,
    "Referer": referrer
}
token_url = f"{referrer}token.php"


def liveit(lastSegment):
    data = {
        "ch": lastSegment,
        "key": "key001"
    }
    r = sess.post(token_url, data=data)
    j = r.json()
    m = re.sub(r'(.{1,2})', r'%\1', j["url"])
    url = unquote(m)
    print(f"> {url}")
    print(f"> {referrer}")
    cmd = f"""vlc --loop "{url}" --http-referrer="{referrer}" --http-user-agent="{agent}" --adaptive-use-access"""
    os.system(cmd)


lastSegment = "bein1"
liveit(lastSegment)
