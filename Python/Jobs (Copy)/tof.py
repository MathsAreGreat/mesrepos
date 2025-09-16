import time
import requests
import os
import logging

url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
FILENAME = "nasa_pic.png"
os.chdir("/home/mohamed/Documents/Projects/Python/Jobs/files")
logging.basicConfig(
    filename="nasa.log",
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_filename(FILENAME):
    directory = "/home/mohamed/Downloads/Files/Images/Jpg/Wallpapers"
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, FILENAME)


def download_pic_of_day():
    try:
        r = requests.get(url)
    except Exception as err:
        print(err)
        time.sleep(5)
        return download_pic_of_day()

    if r.status_code != 200:
        msg = "Network Error !"
        logging.error(msg)
        return 0

    rjs = r.json()
    if "hdurl" not in rjs:
        msg = "No image for today, must be a video"
        logging.error(msg)
        return 0

    picture_url = rjs["hdurl"]
    fn = picture_url.split("/")[-1]
    filename = get_filename(fn)
    msg = f"Already saved picture of the day to {fn}!"
    if not os.path.exists(filename):
        pic = requests.get(picture_url, allow_redirects=True)
        open(filename, "wb").write(pic.content)
        msg = f"New saved picture of the day to {fn}!"
        logging.debug(msg)
        return 1
    logging.info(msg)
    return 1


if __name__ == "__main__":
    download_pic_of_day()
