import os
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')
clr()
print("Running directory: "os.getcwd())
input("Test program running.")
