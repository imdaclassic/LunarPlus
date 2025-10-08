import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox as msgb
import json
import requests

def lunarplus_exists():
    return os.path.isfile("lib/lunarplus.py")

def run_lunarplus():
    script_path = os.path.join("lib", "lunarplus.py")
    try:
        subprocess.Popen([sys.executable, script_path])
        print(f"Started {script_path} in a separate process.")
    except Exception as e:
        print(f"Failed to start {script_path}: {e}")
    finally:
        sys.exit(0)

if lunarplus_exists():
    run_lunarplus()

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

clr()
print("Bootloader: ACTIVE")

ConfirmIs = msgb.askyesno("Confirm Position", "Are you sure that this file is in the lunarV2 folder?")
if not ConfirmIs:
    sys.exit()


msgb.showinfo(
    "Notice & Creator",
    "⚠️ Notice: This is NOT an official extension. It does not interact with the LunarV2 program in any way beyond what a normal user can already do. It is simply a helper plugin.\n\n"
    "👤 Creator: This program was made fully by @imdaclassic on Discord. You are NOT allowed to steal this plugin and rename it for your benefit. "
    "This plugin is open source on GitHub for your own peace of mind."
)

def fetch_lunarplus_index():
    primary_url = "https://raw.githubusercontent.com/imdaclassic/LunarPlus/main/src/index.json"
    fallback_url = "https://raw.githubusercontent.com/imdaclassic/LunarPlus/main/src/index.json"

    for url in (primary_url, fallback_url):
        try:
            print(f"Trying to fetch index from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching {url}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {url}: {e}")

    # If both attempts fail
    return None

print("Getting Version Index...")
try:
    IndexData = fetch_lunarplus_index()
    if IndexData is None:
        raise RuntimeError("Both primary and fallback index fetch attempts failed.")
        input()
except Exception as e:
    print(f"Fatal error: {e}")
    input("Couldn't load index.json. Press Enter to exit, then try again or contact the developer.")
    sys.exit(1)

print("\nLoaded indexes:")
print("---------")
for i in IndexData.get("LunarIndex", []):
    rawlink = i.get("raw-get", "N/A")
    lunarver = i.get("ver", "Unknown")
    print(f"Lunarv2_Ver: {lunarver} | Get-Link: {rawlink}")
print("---------")

msgb.showwarning("Development", "Bootloader/plugin still in development.")

msgb.showinfo("Success", "LunarPlus Extention has been successfully installed, launch it with either START.bat or LP-Manager.bat (Refresh Files to see LP-Manager). To uninstall/update use LP-Manager.bat | If you encounter any issues, please contact @imdaclassic on discord.")
