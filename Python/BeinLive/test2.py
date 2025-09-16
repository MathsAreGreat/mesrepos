import requests
from Crypto.Cipher import AES
import m3u8


referrer = f"https://ilovetoplay.xyz/maxsport.php?id={KEY}"
# ANSI escape codes for terminal manipulation
CURSOR_UP = "\033[1A"
CLEAR_LINE = "\x1b[2K"
UP_CLEAR = CURSOR_UP + CLEAR_LINE
# Setup
sess = requests.Session()
sess.headers.update({"user-agent": USER_AGENT})

sess.headers.update({"Referer": referrer})

u = f"https://webufffit.webhd.ru/lb/{KEY}/index.m3u8"
r = m3u8.load(u)

pl = max(r.data["playlists"], key=lambda e: e["stream_info"]["bandwidth"])
url = pl["uri"]

print(url)
r = m3u8.load(url)
stream_info = r.data["segments"][0]
# Function to download the encryption key


def download_key(key_uri):
    response = sess.get(key_uri)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download the key. Status code: {
                        response.status_code}")

# Function to download the encrypted video segment


def download_encrypted_segment(segment_uri):
    response = sess.get(segment_uri)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(
            "Failed to download the video segment. Status code:",    response.status_code)

# Function to decrypt AES-128 encrypted data


def decrypt_aes128(key, iv, encrypted_data):
    iv_bytes = bytes.fromhex(iv[2:])  # Remove '0x' prefix and convert to bytes
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


# Download the key
key_uri = stream_info['key']['uri']
key = download_key(key_uri)

# Download the encrypted video segment
segment_uri = stream_info['uri']
encrypted_data = download_encrypted_segment(segment_uri)

# Decrypt the segment
iv = stream_info['key']['iv']
decrypted_data = decrypt_aes128(key, iv, encrypted_data)

# Save decrypted data to a file
output_file = 'output.ts'
with open(output_file, 'wb') as f:
    f.write(decrypted_data)

print(f"Decrypted stream saved to {output_file}")
