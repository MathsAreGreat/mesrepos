import os

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
agent = "spis16t3 bot 1.0"

v_url = "https://f6hmx3jswd83sq.nobodywalked.com/hls/0505c4cef0e29ab1-b84a28587bea47d2ba4bb31bef74a63c8024ea46e156330e26e4b58e95c9305f/live.m3u8"
ref = "https://nobodywalked.com"
ref = "https://claplivehdplay.ru/"
v_url = "https://salamus2022.webhd.ru/esx1/primabeinsport2france247/tracks-v1a1/mono.m3u8"

furl = f'"{v_url}" --http-referrer="{ref}" --http-user-agent="{agent}"'

cmd = f"""vlc --loop {furl} --adaptive-use-access"""
os.system(cmd)
