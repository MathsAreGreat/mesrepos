#!/bin/bash

# Colors
GREEN="\e[32m"
RESET="\e[0m"

LINK_FILE="/home/mohamed/Documents/datas/Databases/instas.txt"
DOWNLOAD_DIR="/home/mohamed/.Kindas/Instagram"
mkdir -p "$DOWNLOAD_DIR"
cd "$DOWNLOAD_DIR"

echo -e "${GREEN}Updating packages...${RESET}"

touch downloaded.txt

rg '/(reel|video)/' "$LINK_FILE" | while IFS= read -r line; do
    if ! grep -Fxq "$line" downloaded.txt; then
        yt-dlp -o "%(channel)s/%(id)s==%(upload_date)s.%(ext)s" --cookies-from-browser firefox "$line"
    fi
done

echo -e "${GREEN}All done!${RESET}"
