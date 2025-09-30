import os
import subprocess
import sys
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
import tkinter as tk
from tkinter import messagebox as msgb
import json
import requests
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')
clr()
print("Bootloader: ACTIVE")

ConfirmIs = msgb.askyesno("Confirm Position", "Are you sure that this file is in the lunarV2 folder?")
if not ConfirmIs:
    sys.exit()
msgb.showwarning("Notice", "Notice: This is NOT an official plugin. It does not interact with the LunarV2 program in any way beyond what a normal user can already do. It is simply a helper plugin.")

def fetch_lunarplus_index():
    url = "https://github.com/imdaclassic/LunarPlus-Plugin/raw/refs/heads/main/src/index.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
print("Getting Version Index...")
IndexData = fetch_lunarplus_index()
if IndexData == None:
    input("Coudnt Load Index, try again, else contact developer with error above.")
    sys.exit()
print("\nloaded indexes:")
print("---------")
for i in IndexData["LunarIndex"]:
    rawlink = i["raw-get"]
    lunarver = i["ver"]
    print(f"Lunarv2_Ver: {lunarver} | Get-Link: {rawlink}")
print("---------")

input("Bootloader/plugin still in development.")
