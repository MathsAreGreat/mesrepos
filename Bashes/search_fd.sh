#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 pattern1 [pattern2 ...]"
    exit 1
fi

cd ~

cmd="fd -t f -i -a"
for pattern in "$@"; do
    cmd="$cmd | rg -i \"$pattern\""
done
cmd="$cmd | sort"

mapfile -t files < <(eval "$cmd")

if [ "${#files[@]}" -eq 0 ]; then
    echo "No matching files found."
    exit 0
fi

# Group files by directory
declare -A grouped
for file in "${files[@]}"; do
    dir=$(dirname "$file")
    name=$(basename "$file")
    grouped["$dir"]+="$name"$'\n'
done

# Index tracking
i=0
declare -a file_index

# Display grouped files with indexes
for dir in "${!grouped[@]}"; do
    echo "$dir/"
    while IFS= read -r filename; do
        if [ -n "$filename" ]; then
            echo "[$i] $filename"
            file_index[$i]="$dir/$filename"
            ((i++))
        fi
    done <<< "${grouped[$dir]}"
    echo "---------------------------"
done

# Prompt user to open a file
echo -n "Enter number to open file (or press Enter to skip): "
read index

if [[ "$index" =~ ^[0-9]+$ ]] && [ "$index" -ge 0 ] && [ "$index" -lt "${#file_index[@]}" ]; then
    file="${file_index[$index]}"
    xdg-open "$file" >/dev/null 2>&1 &
    echo "Opening $file..."
else
    echo "No file opened."
fi
