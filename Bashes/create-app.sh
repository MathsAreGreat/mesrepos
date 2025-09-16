#!/bin/bash

# Colors
RED='\033[0;31m'
NC='\033[0m' # No Color

# Moves
UP="\033[1A"
WIPE="\x1b[2K"
CLEAR="$UP$WIPE"

# Ask for app name until it's non-empty
read -p "App name (required): " appname
while [[ -z "$appname" ]]; do
    echo -e "$CLEAR${RED}Error: App name cannot be empty!${NC}"
    read -p "App name (required): " appname
    echo -e "$CLEAR$CLEAR"
done

echo "App name (required): $appname"

# Prompt user for inputs
read -p "App comment (Optional): " appcomment

# Fallback icon
appvalue=${appname,,}
appcomment=${appcomment:-"No Comment"}

# Desktop file path
desktop_file="$HOME/.local/share/applications/$appvalue.desktop"
appimage_path="/home/mohamed/Downloads/Files/Apps/$appvalue"

# Create the applications directory if needed
mkdir -p ~/.local/share/applications

# Write the .desktop file
cat > "$desktop_file" << EOF
[Desktop Entry]
Name=$appname
Comment=$appcomment
Exec=$appimage_path
Icon=$appvalue
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=true
EOF

# Make AppImage executable (safely)
chmod +x "$appimage_path"

mv /home/mohamed/Downloads/*.png ~/.local/share/icons/

update-desktop-database ~/.local/share/applications
echo "✔️  Desktop entry created: $desktop_file"
