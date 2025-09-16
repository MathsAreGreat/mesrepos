#!/bin/bash

URL="$1"
vid="$2"
OUTDIR="$HOME/Documents/Files"

# If no $vid provided, extract it from the URL
if [[ -z "$vid" ]]; then
    filename=$(echo "$URL" | awk -F '[=/?]' '{print $NF}')
    basename="${filename#embed-}"   # remove "embed-" prefix
    vid="${basename%.html}"  
fi

FILE="$OUTDIR/$vid.json"

# If file already exists, exit
if [[ -f "$FILE" ]]; then
    echo "File already exists: $FILE"
else
    # Ensure output directory exists
    mkdir -p "$OUTDIR"

    # Extract metadata and filter only desired fields
    yt-dlp --dump-json "$URL" | jq '{title,thumbnail,url,duration,tbr,width,height}' > "$FILE"
    echo "Saved metadata: $FILE"
fi

if [[  ! -f "$FILE" ]]; then
    echo "{}" > "$FILE"
fi