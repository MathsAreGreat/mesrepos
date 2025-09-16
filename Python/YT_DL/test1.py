import requests

u = "https://wsxcvx6.zfghrew10.shop/to3qwamzkjvsy46b3v3wxlpydct3nfntf6a6yefv2ywejpu2ihov6s5n5q2q/v.mp4"

r = requests.get(u, stream=True)

print(r.headers)
