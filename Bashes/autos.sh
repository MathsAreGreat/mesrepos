#!/bin/bash

# Colors
GREEN="\e[32m"
RESET="\e[0m"

echo -e "${GREEN}Updating pacman packages...${RESET}"

# Run the steps
sudo pacman -Syu --noconfirm

echo -e "${GREEN}Remove unused packages...${RESET}"
sudo pacman -Rns $(pacman -Qdtq) --noconfirm
sudo pacman -Scc --noconfirm

echo -e "${GREEN}Updating yay packages...${RESET}"

yay -Syu --noconfirm
yay -Sc --noconfirm
yay -Yc --noconfirm

echo -e "${GREEN}All done!${RESET}"
