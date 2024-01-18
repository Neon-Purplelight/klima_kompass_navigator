# init_script.py

import os

from utils import dataManager as dm

# URLs und Ziele für die zu ladenden Dateien
files_to_download = {
    "https://files.ufz.de/~drought/SMI_Gesamtboden_monatlich.nc": "data/originalData/SMI_Gesamtboden_monatlich.nc",
    "https://files.ufz.de/~drought/SMI_Oberboden_monatlich.nc": "data/originalData/SMI_Oberboden_monatlich.nc"
}

for url, destination in files_to_download.items():
    if not os.path.exists(destination):
        print(f"Downloading {url} to {destination}...")
        dm.download_file(url, destination)

print("All files are ready.")
