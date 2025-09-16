#!/bin/bash

# ───────────────────────────────
# Script: youtube_audio_mux.sh
# Purpose: Download YouTube videos, extract audio streams,
#          and mux them into final MKV with language metadata
# Usage: ./youtube_audio_mux.sh <video_id1> <video_id2> ...
# ───────────────────────────────

if [[ $# -eq 0 ]]; then
    echo "Error: No video IDs/URLs provided."
    echo "Usage: $0 <video_id1> <video_id2> ..."
    exit 1
fi

OUTDIR="$HOME/Videos"

for vid in "$@"; do
    echo "───────────────────────────────"
    echo " Processing video: $vid"
    echo "───────────────────────────────"

    # ───── Directories and paths ─────
    LOGS_PATH="$HOME/Documents/backup_ids_$vid.txt"
    OUTPUT_PATH="$OUTDIR/$vid.%(ext)s"
    CLEAN_PATH="$OUTDIR/$vid.mkv"
    URL="https://www.youtube.com/watch?v=$vid"  
    FILE="$OUTDIR/$vid.json"
    output_ids="$OUTDIR/output_$vid.txt"

    mkdir -p "$(dirname "$LOGS_PATH")" "$OUTDIR"

    # ───── Download metadata if not already present ─────
    if [[ -f "$FILE" ]]; then
        echo "File already exists: $FILE"
    else
        yt-dlp --dump-json "$URL" \
            | jq '{title, uploader_id, upload_date, formats: [.formats[] | {format_id, language, format_note}]}' \
            > "$FILE"
        echo "Saved metadata: $FILE"
    fi

    # ───── Collect format IDs ─────
    echo "bestvideo" > "$LOGS_PATH"

    jq -r '.formats[] | select(.format_id | test("^251")) | .format_id' "$FILE" >> "$LOGS_PATH" || {
        echo "Warning: No format IDs starting with 251 found in metadata JSON."
    }

    if [[ ! -s "$LOGS_PATH" || $(wc -l < "$LOGS_PATH") -le 1 ]]; then
        echo "Error: No valid audio formats found in $LOGS_PATH."
        continue
    fi

    FORMAT=$(tr '\n' '+' < "$LOGS_PATH" | sed 's/+$//')

    # ───── Extract language and format notes ─────
    ids=$(jq -r '.formats[] | select(.format_id == "251") | [.language, .format_note] | join("=")' "$FILE")
    if [[ -z "$ids" || $ids == "" ]]; then
        ids=$(jq -r '.formats[] | select(.format_id | startswith("251")) | [.language, .format_note] | join("=")' "$FILE")
    fi
    echo "$ids" > "$output_ids"

    # ───── Prepare final output path ─────
    upload_date=$(jq -r '.upload_date' "$FILE")
    title=$(jq -r '.title' "$FILE" | sed 's/[\/:*?"<>|]/_/g')
    uploader=$(jq -r '.uploader_id' "$FILE" | sed 's/[\/:*?"<>|]/_/g')
    FINAL_DIR="${OUTDIR}/Youtube/${uploader:1}"
    mkdir -p "$FINAL_DIR"
    FINAL_OUT="${FINAL_DIR}/${upload_date}_${title} (${vid}).mkv"

    # ───── Download + mux ─────
    if [[ -f "$FINAL_OUT" ]]; then
        echo "Already processed: $FINAL_OUT"
    else
        yt-dlp -f "$FORMAT" --audio-multistreams "$URL" \
            -o "$OUTPUT_PATH" --merge-output-format mkv \
            --cookies-from-browser firefox --write-sub --sub-langs ar,fr,en,-live_chat || {
            echo "Error: Download failed for $URL."
            continue
        }
        echo "Download completed successfully for $URL."

        # ───── Build ffmpeg command ─────
        inputs=" -i \"$CLEAN_PATH\""
        maps=" -map 0:v -c:v copy"

        idx=0
        while IFS='=' read -r language format_note || [ -n "$language" ]; do
            [[ -z "$language" ]] && continue
            maps+=" -map 0:a:$idx -c:a copy -metadata:s:a:$idx language=$language -metadata:s:a:$idx title=\"$format_note\""
            idx=$((idx + 1))
        done < "$output_ids"

        sub_idx=0
        for f in "$OUTDIR/$vid"*.vtt; do
            [[ -e "$f" ]] || continue
            inputs+=" -i \"$f\""
            lang="${f%.*}"
            lang="${lang##*.}"
            maps+=" -map $((sub_idx+1)):0 -c:s srt -metadata:s:s:$sub_idx language=$lang"
            sub_idx=$((sub_idx+1))
        done

        cmd="ffmpeg $inputs $maps -movflags +faststart \"$FINAL_OUT\""
        bash -c "$cmd" || {
            echo "Error: ffmpeg command failed for $vid."
            continue
        }
    fi

    # ───── Cleanup ─────
    rm -rf "$output_ids" "$OUTDIR/$vid"*
    echo "Finished processing: $vid"
done
