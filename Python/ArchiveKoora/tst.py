import requests

# u = "https://a2.file-hd.com/hls2/02/00010/qc3pjombbbjh_,l,h,.urlset/master.m3u8?t=cbqcZDIpTRIWuihWS9AMyhm_ZveUgUXL-jiZOhnA5L8&s=1747345631&e=10800&f=52896&i=105.157&sp=2500"
# t = "live"
# c = "key"
# r = None
# dt = (
#     u,
#     f"{t}.[%(height)sp].({c}).mp4",
#     r
# )


# plus = "--downloader ffmpeg --hls-use-mpegts"
# download_m3u8_with_aria2c(*dt, plus=plus)

sess = requests.Session()

link = "https://bestb.stream/e/add.php"
headers = {
    "Referer": "https://streamup.ws/",
}
p = sess.post(
    link,
    data={
        "filecode": {
            "title": "",
            "thumbnail": "https://hls2-c1-cdn1-stg2.streamupcdn.com/thumbnail/wE8iV3I9D9kPS2O7foJCfhUq65An4W/MxQwKavTLhW7l.jpg",
            "streaming_url": "https://hls2-c1-cdn1-stg2.streamupcdn.com/hls/woUwk8jQPJstWNx8hErjwMvHUWBcth/master.m3u8",
            "vast_ads": "",
            "filecode": "MxQwKavTLhW7l",
        }
    },
)

print(p)
