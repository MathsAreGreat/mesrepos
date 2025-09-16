from deemix import generateDownloadObject
from deemix.settings import load as loadSettings
from deemix.downloader import Downloader

# Set Deezer ARL (needed for authentication)
ARL_TOKEN = "b39a94a8625463bbd032001aedd364dd4643f4e9758e72565629c9bc8cb35903e9fe9282cf70e39f1d3ed88fd0faaaac5de0fc14fe1abcb6087e8491a129f77c2a84f1d0803719e51136b86290c160a589bf99bb39c8a969d24ee448dd485326"  # Get your ARL from Deezer cookies

# File ID (replace with actual track ID from Deezer)
file_id = 2927577241

# Load default settings
settings = loadSettings()

# Set download path
settings['downloadLocation'] = "./downloads"

# Create a download object
download_object = generateDownloadObject(
    "https://www.deezer.com/en/playlist/1498086991", ARL_TOKEN, settings)

# Initialize downloader
downloader = Downloader(settings)
downloader.startDownload(download_object)

print(f"Downloading track {file_id}...")
