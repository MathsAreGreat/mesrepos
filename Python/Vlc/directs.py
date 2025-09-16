import os
import sys

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
refs = {
    "sn": "https://snrtlive.ma/",
    "sh": "https://sba.net.ae/",
    "AD": "https://player.mangomolo.com",
    "KS": "https://www.alkass.net/",
    "ya": "https://www.yallateri.com"
}

keys = {
    "sn_ar": "https://cdnamd-hls-globecast.akamaized.net/live/ramdisk/arriadia/hls_snrt/arriadia-avc1_1500000=4-mp4a_130400_qad=1.m3u8",
    "sh_ar": "https://svs.itworkscdn.net/smc4sportslive/smc4tv.smil/smc4sportspublish/smc4tv_source/chunks.m3u8",
    "sn_al": "https://cdnamd-hls-globecast.akamaized.net/live/ramdisk/al_aoula_inter/hls_snrt/al_aoula_inter-avc1_1500000=4-mp4a_130400_qad=1.m3u8",
}

for i in range(10):
    j = i+1
    keys[f"ya{j}"] = f"https://live.simogames.pro/hls/yallalive{j}/index.m3u8"

try:
    key = sys.argv[1]
    r = key[:2]
    url = keys[key]
    ref = refs[r]
except:
    url = "https://p2.kora44.site/broadcast/hz0OhbsOAbF0bqg4IWcV2A/1728762996/1728762735/1/bein02.m3u8"
    url = "https://p2.kora44.site/broadcast/1qLvktL2UyjxZUtaipb0JQ/1728767850/1728767589/1/bein02.m3u8"
    ref = "https://super-koora.com/"

print(url)
print(ref)
cmd = f"""vlc --loop "{url}" --http-referrer="{ref}" """
cmd += f"""--http-user-agent="{agent}" --adaptive-use-access"""
os.system(cmd)
