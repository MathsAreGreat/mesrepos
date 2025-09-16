#!/bin/bash

# === 📝 Editable Section ===
TARGET_DIR="/home/mohamed/Documents/Projects"
TARGET_USER="mohamed"
FILE_TYPES=("*.py" "*.sh")
EXCLUDE_PATHS=("*/.venv/*" "*/.git/*" "*/__pycache__/*")
# ===========================

echo "Checking files under: $TARGET_DIR at $(date)"
MODIFIED_COUNT=0

# Start building the find command as an array
FIND_CMD=(find "$TARGET_DIR" -type f)

# Exclude paths like .venv and .git
for pattern in "${EXCLUDE_PATHS[@]}"; do
    FIND_CMD+=( ! -path "$pattern" )
done

# Add name filters for specific file types
FIND_CMD+=( \( )
for ext in "${FILE_TYPES[@]}"; do
    FIND_CMD+=( -name "$ext" -o )
done
unset 'FIND_CMD[${#FIND_CMD[@]}-1]'  # Remove trailing -o
FIND_CMD+=( \) -readable -print0 )

# Execute find and process matching files
"${FIND_CMD[@]}" | while IFS= read -r -d '' file; do
    if grep -qP "/home/mohamed/)[^/]+/" "$file"; then
        perl -i -pe "s|/home/mohamed/)[^/]+/|/home/mohamed/|g" "$file"
        echo "Modified: $file"
        ((MODIFIED_COUNT++))
    fi
done

# Report result
if [[ $MODIFIED_COUNT -eq 0 ]]; then
    echo "No files needed modification. Exiting."
else
    echo "$MODIFIED_COUNT file(s) were modified."
fi
