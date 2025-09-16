import m3u8
from pathlib import Path

from Mido.variables import run_tasks, print

headers = {}

url = "https://jxoxkplay.xyz/"
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
headers.update({"user-agent": USER_AGENT})
headers.update({"Referer": url})
u = "https://top2new.newkso.ru/top2/bet8210756/mono.m3u8"

data = m3u8.load(u, headers=headers).data

print(data)
