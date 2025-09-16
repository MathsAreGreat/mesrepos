import subprocess
import json
import sys
import time


def get_media_duration(filepath):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
                "format=duration", "-of", "json", filepath],
            capture_output=True,
            text=True
        )
        duration = json.loads(result.stdout)["format"]["duration"]
        return float(duration)
    except:
        return -1


def play_last_minute(filepath, nb=10):
    duration = get_media_duration(filepath)
    if duration < 0:
        return 0
    start_time = max(duration - nb, 0)
    subprocess.run([
        "vlc",
        "--start-time", str(start_time),
        "--play-and-exit",
        "--fullscreen",
        filepath
    ], capture_output=True, text=True)
    return 1


time.sleep(1)
try:
    v = sys.argv[1]
except:
    v = "Live"

video_path = f"/home/mohamed/Videos/Ts/{v}.ts"

# Update with the path to your video file
while True:
    if play_last_minute(video_path):
        time.sleep(2)
