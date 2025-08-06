# New - auto updater module for Spryzen - update the program if there is a new version
import subprocess
import requests
from colorama import Fore, Style, init
init(autoreset=True)

# Checking for current local version
def get_local_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"
    
# Checking for current remote version
def get_remote_version(url):
    #Get the current version from url request to Github
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except requests.RequestException:
        return None
    
#Update function
def updater():
    remote_version = get_remote_version()
    print(Fore.GREEN + Style.BRIGHT + f"[*] Update to the latest version: {remote_version}")
    subprocess.run(["git", "pull"], check=True)
    print(Fore.GREEN + Style.BRIGHT + "[✓] Spryzen updated. Please restart the tool.")
    exit(0)

#Checking update function
def check_update():
    local_version = get_local_version()
    remote_url = "https://raw.githubusercontent.com/Sown0205/Spryzen/v.1.1/version.txt"
    remote_version = get_remote_version(remote_url)
      
    if not remote_version:
        print(Fore.YELLOW + "[!] Could not check for updates (offline or unreachable).")
        return
    
    if local_version != remote_version:
        print(Fore.YELLOW + Style.BRIGHT + f"[!] Update is available: {local_version} → {remote_version}")
        print(Fore.RESET + "You can pull latest version on Github: git pull origin main")
        print("Or you can update it automatically here\n")
        prompt = input(Fore.YELLOW + Style.BRIGHT + "Do you want to update this program ?(yes/no): ").strip().lower()

        if prompt == "yes":
            updater()

        elif prompt == "no":
            print(Fore.YELLOW + Style.BRIGHT + "[!] Latest version will have new features for the program")
            print(Fore.YELLOW + Style.BRIGHT + "It is recommended that you update the program to the latest version")

        else:
            print(Fore.RED + Style.BRIGHT + "Invalid command")

    else:
        print(Fore.CYAN + Style.BRIGHT + "Your Spryzen is on the latest version")