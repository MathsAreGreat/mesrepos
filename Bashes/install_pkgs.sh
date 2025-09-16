#!/bin/bash

packages_path="/home/mohamed/Documents/datas/Databases"

# Define python packages
mapfile -t PY_PACKAGES < "$packages_path/py_packages.txt"

# Define appimages
mapfile -t PR_PACKAGES < "$packages_path/pr_packages.txt"

# Define python packages
mapfile -t SYS_PACKAGES < "$packages_path/sys_packages.txt"

# Define pacman and yay packages
mapfile -t PACMAN_PACKAGES < "$packages_path/pc_packages.txt"
mapfile -t YAY_PACKAGES < "$packages_path/yay_packages.txt"


# Colors
GREEN="\e[32m"
RESET="\e[0m"

# Function to install pacman packages
install_pacman_packages() {
    for pkg in "${PACMAN_PACKAGES[@]}"; do
        if ! pacman -Qi "$pkg" &>/dev/null; then
            sudo pacman -S --noconfirm "$pkg"
        fi
    done
}

# Function to install Python packages using pip
install_py_packages() {
    for pkg in "${PY_PACKAGES[@]}"; do
        if ! uv pip show "$pkg" &> /dev/null; then
            echo -e "Installing ${pkg}..."
            uv pip install "$pkg"
        fi
    done
}


# Function to download the latest Arch Linux ISO
download_iso() {
    DOWNLOAD_DIR="/home/mohamed/Downloads/Files/Apps"
    VERSION_DIR="$DOWNLOAD_DIR/versions"
    mkdir -p "$VERSION_DIR"

    BASE_URL="https://mirror.rackspace.com/archlinux/iso/latest"
    SHA_FILE="$BASE_URL/sha256sums.txt"

    # Get the filename of the ISO
    iso_filename=$(curl -s "$SHA_FILE" | awk '{print $2}' | head -1)

    if [[ -z "$iso_filename" ]]; then
        echo "❌ Failed to fetch ISO filename from $SHA_FILE"
        return 1
    fi

    iso_url="$BASE_URL/$iso_filename"
    version_marker="$VERSION_DIR/$iso_filename"
    final_path="$DOWNLOAD_DIR/arch.iso"

    if [[ -f "$version_marker" ]]; then
        echo "⚠️  Latest Arch ISO ($iso_filename) already exists — skipping download"
        return 0
    fi

    echo "⬇️  Downloading latest Arch ISO: $iso_filename"
    if curl -L "$iso_url" -o "$final_path"; then
        echo "✅ Downloaded and saved as: $final_path"
        touch "$version_marker"
    else
        echo "❌ Failed to download ISO from $iso_url"
        return 2
    fi
}


# Function to install Python packages using pip
download_install_appimages() {
    DOC="/home/mohamed/Downloads/Files/Apps"
    mkdir -p "$DOC/versions"
    for repo in "${PR_PACKAGES[@]}"; do
        appname="$(basename "$repo")"
        app_path="$DOC/$appname"
        echo "Processing $repo..."
        # Get latest release info from GitHub API
        url=$(curl -s "https://api.github.com/repos/$repo/releases/latest" \
            | grep "browser_download_url" \
            | grep -iE "AppImage" \
            | grep -iE "x86_64|amd64|linux-x64" \
            | cut -d '"' -f 4 \
            | head -n 1)

        # Get the file name from the URL
        filename=$(basename "$url")
        file_path="$DOC/versions/$filename"

        if [[ -z "$url" ]]; then
            echo "❌ No AppImage found for $repo"
            continue
        fi


        # Skip if file already exists
        if [[ -f "$file_path" ]]; then
            echo "⚠️  $appname latest version already exists — skipping download"
            continue
        fi

        # Download the AppImage
        echo "⬇️  Downloading $filename"
        curl -L "$url" -o "$file_path"
        echo "✅ Downloaded : $filename"
        cp "$file_path" "$app_path"
        chmod +x "$app_path"

        echo "✅ Saved as: $appname"
        rm -rf $file_path
        touch $file_path
        echo
    done
}

upgrade_outdated_py_packages() {
    echo -e "${GREEN}Upgrading outdated Python packages...${RESET}"
    outdated_pkgs=$(uv pip list --outdated | awk 'NR>2 {print $1}')
    for pkg in $outdated_pkgs; do
        echo -e "Upgrading ${pkg}..."
        uv pip install -U "$pkg"
    done
}

# Function to install yay
install_yay() {
    if ! command -v yay &>/dev/null; then
        echo -e "${GREEN}Installing yay...${RESET}"
        cd /tmp || exit 1
        git clone https://aur.archlinux.org/yay.git
        cd yay || exit 1
        makepkg -si --noconfirm
    fi
}


# Function to install yay packages
install_yay_packages() {
    install_yay
    echo
    for pkg in "${YAY_PACKAGES[@]}"; do
        [[ -z "$pkg" || "$pkg" =~ ^[[:space:]]*$ ]] && continue
        if ! yay -Qi "$pkg" &>/dev/null; then
            yay -S --noconfirm "$pkg"
        fi
    done
}


# Function to install yay packages
start_packages() {
    for pkg in "${SYS_PACKAGES[@]}"; do
        [[ -z "$pkg" || "$pkg" =~ ^[[:space:]]*$ ]] && continue
        sudo systemctl start "$pkg"
        sudo systemctl enable "$pkg"
    done
}


echo -e "${GREEN}Installing start packages...${RESET}"
echo "===================================="
download_install_appimages
download_iso
echo "===================================="
install_yay_packages
echo "===================================="
echo -e "${GREEN}yay pkgs done!${RESET}"
install_pacman_packages
echo "===================================="
echo -e "${GREEN}pacman pkgs done!${RESET}"
install_py_packages
upgrade_outdated_py_packages
echo "===================================="
echo -e "${GREEN}Python pkgs done!${RESET}"