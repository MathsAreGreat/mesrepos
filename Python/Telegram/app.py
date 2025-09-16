import subprocess
from pathlib import Path

# Define file path and caption


def goo(caption, telegram_target, file_path):
    # Build the command
    command = f"""telegram-upload --caption "{caption}" --to "{telegram_target}" "{file_path}" -d"""
    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Failed to upload {e}")
        print(file_path)


while True:

    datas = []

    parent_path = Path("Files/Docs")
    files = sorted(parent_path.rglob("*"), key=lambda f: f.stem)
    telegram_target = "https://t.me/+M2kiuz7a_9RiYWJk"
    telegram_target = "https://t.me/+slSEN_0UV5NmMTBk"
    for file_path in files:
        caption = file_path.stem
        datas.append((caption, telegram_target, file_path))

    parent_path = Path("Files/YTS")
    files = sorted(parent_path.rglob("*.mp4"), key=lambda f: f.stem)
    telegram_target = "https://t.me/+prQYogIOyVIzODZk"
    for file_path in files:
        caption = file_path.stem
        datas.append((caption, telegram_target, file_path))

    parent_path = Path("Files/TOPS")
    files = sorted(parent_path.rglob("*.mp4"), key=lambda f: f.stem)
    files += sorted(parent_path.rglob("*.mkv"), key=lambda f: f.stem)
    telegram_target = "https://t.me/+103WHtuV7KpkNTE0"
    for file_path in files:
        caption = file_path.stem
        datas.append((caption, telegram_target, file_path))

    if datas:
        for dt in datas:
            goo(*dt)
