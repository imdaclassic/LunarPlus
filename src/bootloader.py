import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgb
import json
import requests
from tqdm import tqdm

def lunarplus_exists():
    return os.path.isfile("lib/lunarplus.py")
def create_lv2_version_file(content: str):
    os.makedirs("lib", exist_ok=True)
    file_path = os.path.join("lib", "lv2_version")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

def run_lunarplus():
    script_path = os.path.join("lib", "lunarplus.py")
    try:
        res = msgb.askyesno("Confirm", "lunarplus.py is already installed, do you want to remove and continue install?")
        if res:
            os.remove("lib/lunarplus.py")
        else:
            sys.exit(0)
    except Exception as e:
        print(f"Failed to delete {script_path}: {e}")
        msgb.showerror("Error!", f"Failed to delete {script_path}: {e}")
        sys.exit(0)

if lunarplus_exists():
    run_lunarplus()

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame = ttk.Frame(canvas)
        self.window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self.window, width=e.width)
        )

def download_lunarplus(url, lib_folder="lib", filename="lunarplus.py"):
    os.makedirs(lib_folder, exist_ok=True)
    filepath = os.path.join(lib_folder, filename)

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with open(filepath, "wb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc=filename
    ) as bar:
        for data in response.iter_content(block_size):
            f.write(data)
            bar.update(len(data))

    print(f"\nDownload complete: {filepath}")
    return filepath

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
            msgb.showerror("Error!", f"Network error fetching {url}: {e}")
            sys.exit(0)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {url}: {e}")
            msgb.showerror("Error!", f"Error decoding JSON from {url}: {e}")
            sys.exit(0)

    # If both attempts fail
    return None

print("Getting Version Index...")
try:
    IndexData = fetch_lunarplus_index()
    if IndexData is None:
        msgb.showerror("indx error", "Index Error! None type proscribed")
        raise RuntimeError("Both primary and fallback index fetch attempts failed.")
except Exception as e:
    print(f"Fatal error: {e}")
    msgb.showerror("Error!", f"Fatal error: {e}")
    sys.exit(0)

print("\nLoaded indexes:")
print("---------")
for i in IndexData.get("LunarIndex", []):
    rawlink = i.get("raw-get", "N/A")
    lunarver = i.get("ver", "Unknown")
    print(f"Lunarv2_Ver: {lunarver} | Get-Link: {rawlink}")
print("---------")

SelectedVersion = ""
def GetVersion():
    root = tk.Tk()
    root.title("Select LunarPlus Version")
    #root.geometry("500x500")
    #root.resizable(0,0)
    text = tk.Label(root, text="Click on your current lunarV2 version below", font=('TkDefaultFont', 12))
    text.pack(pady=10)
    def rtn(ver):
        global SelectedVersion
        res = msgb.askyesno(f"Selected {ver}?", f"Are you sure you want to load {ver}?")
        if res:
            root.destroy()
            SelectedVersion = ver
            create_lv2_version_file(SelectedVersion)
            return
    sf = ScrollableFrame(root)
    for i in IndexData.get("LunarIndex", []):
        lunarver = i.get("ver", "Unknown")
        button = tk.Button(root, text=f"V{lunarver}", width=50, command=lambda: rtn(lunarver))
        button.pack(pady=2)
    sf.pack(fill="both", expand=True)

    root.mainloop()
GetVersion()
print(f"You selected lunarV2 version {SelectedVersion}")
get = ""
for i in IndexData.get("LunarIndex", []):
    rawlink = i.get("raw-get", "N/A")
    lunarver = i.get("ver", "Unknown")
    if lunarver == SelectedVersion:
        get = rawlink
print(f"Downloading latest LunarPlus from link: {get}")

download_lunarplus(get)

print("Rewriting START.bat ... (Downloading NewStart.bat)")
def update_start_bat(
    url="https://raw.githubusercontent.com/imdaclassic/LunarPlus/refs/heads/main/src/ext/NewStart.bat",
    filename="START.bat"
):
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise error if download fails

        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"{filename} has been updated successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {e}")
        msgb.showerror("Error!", f"Failed to download file: {e}")
        sys.exit(0)
    except OSError as e:
        print(f"Failed to write file: {e}")
        msgb.showerror("Error!", f"Failed to write file: {e}")
        sys.exit(0)
update_start_bat()
print("START.bat done.")

print("LunarPlus installed!")

msgb.showwarning("Development", "Bootloader/plugin still in development.")

msgb.showinfo("Success", "LunarPlus Extention has been successfully installed, launch it with either START.bat or LP-Manager.bat (Refresh Files to see LP-Manager). To uninstall/update use LP-Manager.bat | If you encounter any issues, please contact @imdaclassic on discord.")
