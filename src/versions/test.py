from tkinter import messagebox as msgb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mode", help="Custom mode tag", default="default")
args = parser.parse_args()

if args.mode == "manage":
    print("Running in MANAGE mode!")
elif args.mode == "select":
    print("Running in SELECT mode!")

msgb.showwarning("Test", "This extention version is a test!")
