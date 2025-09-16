#!/bin/bash

echo "=== vCard Generator (v3.0) ==="

read -p "Full name (FN): " fn
[[ "$fn" == "none" ]] && fn=""

read -p "Nickname (or 'none'): " nick
[[ "$nick" == "none" ]] && nick=""

read -p "Organization (ORG) or 'none': " org
[[ "$org" == "none" ]] && org=""

read -p "Title (e.g. Developer) or 'none': " title
[[ "$title" == "none" ]] && title=""

# === PHONE ===
echo "Phone (TEL), type 'none' to skip"
read -p "  Type (CELL, HOME, WORK, FAX, PAGER, VOICE, TEXT) or 'none': " phone_type
if [[ "$phone_type" != "none" ]]; then
  valid_tel=("CELL" "HOME" "WORK" "FAX" "PAGER" "VOICE" "TEXT")
  while [[ ! " ${valid_tel[*]} " =~ " $phone_type " ]]; do
    echo "  ❌ Invalid type. Choose from: ${valid_tel[*]}"
    read -p "  Type: " phone_type
  done
  read -p "  Number: " phone
fi

# === EMAIL ===
echo "Email, type 'none' to skip"
read -p "  Type (HOME, WORK, INTERNET) or 'none': " email_type
if [[ "$email_type" != "none" ]]; then
  valid_email=("HOME" "WORK" "INTERNET")
  while [[ ! " ${valid_email[*]} " =~ " $email_type " ]]; do
    echo "  ❌ Invalid type. Choose from: ${valid_email[*]}"
    read -p "  Type: " email_type
  done
  read -p "  Address: " email
fi

# === ADDRESS ===
echo "Address (ADR), type 'none' to skip"
read -p "  Type (HOME, WORK, POSTAL, PARCEL) or 'none': " adr_type
if [[ "$adr_type" != "none" ]]; then
  valid_adr=("HOME" "WORK" "POSTAL" "PARCEL")
  while [[ ! " ${valid_adr[*]} " =~ " $adr_type " ]]; do
    echo "  ❌ Invalid type. Choose from: ${valid_adr[*]}"
    read -p "  Type: " adr_type
  done
  read -p "  Street: " street
  read -p "  City: " city
  read -p "  Region: " region
  read -p "  Postal Code: " zip
  read -p "  Country: " country
fi

# === OTHER FIELDS ===
read -p "Website URL (or 'none'): " url
[[ "$url" == "none" ]] && url=""

read -p "Birthday (YYYYMMDD) or 'none': " bday
[[ "$bday" == "none" ]] && bday=""

read -p "Note (or 'none'): " note
[[ "$note" == "none" ]] && note=""

# === OUTPUT vCard ===
output="contact.vcf"
echo "BEGIN:VCARD" > "$output"
echo "VERSION:3.0" >> "$output"
[[ -n "$fn" ]] && echo "FN:$fn" >> "$output"
[[ -n "$nick" ]] && echo "NICKNAME:$nick" >> "$output"
[[ -n "$org" ]] && echo "ORG:$org" >> "$output"
[[ -n "$title" ]] && echo "TITLE:$title" >> "$output"
[[ -n "$phone_type" && "$phone_type" != "none" && -n "$phone" ]] && echo "TEL;TYPE=$phone_type:$phone" >> "$output"
[[ -n "$email_type" && "$email_type" != "none" && -n "$email" ]] && echo "EMAIL;TYPE=$email_type:$email" >> "$output"
if [[ -n "$adr_type" && "$adr_type" != "none" ]]; then
  echo "ADR;TYPE=$adr_type:;;$street;$city;$region;$zip;$country" >> "$output"
fi
[[ -n "$url" ]] && echo "URL:$url" >> "$output"
[[ -n "$bday" ]] && echo "BDAY:$bday" >> "$output"
[[ -n "$note" ]] && echo "NOTE:$note" >> "$output"
echo "REV:$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$output"
echo "END:VCARD" >> "$output"

echo "✅ vCard saved to '$output'"
