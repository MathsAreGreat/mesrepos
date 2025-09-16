from Mido.variables import download_m3u8_with_aria2c

# create an instance of the Cinemagoer class
u = "https://vk6-30.vkuser.net/video.m3u8?cmd=videoPlayerCdn&expires=1756951382093&srcIp=196.74.24.15&pr=40&srcAg=CHROME&ms=95.142.206.42&mid=9303755335935&type=2&sig=nNpJVKFLkYE&ct=8&urls=45.136.20.193%3B45.136.21.154&clientType=13&zs=65&id=8519762381567"

u = "https://vk.com/video_ext.php?oid=721415423&id=456242364&hash=e4373b5c9c004c6f&hd=1"

download_m3u8_with_aria2c(
    u, "/home/mohamed/Documents/Projects/Python/CimDB/test1.[%(height)sp].mp4"
)
