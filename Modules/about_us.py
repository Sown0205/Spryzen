from colorama import Fore, Style
from time import sleep
import os

#import utils module
from Modules import utils

# Main funtion
def run():
    lines = [
        Fore.YELLOW + Style.BRIGHT + "About this program:",
        Fore.RESET + Style.BRIGHT + "- This program has 3 main tools:",
        Fore.RESET + Style.BRIGHT + "1. Cryptography Tool - encrypt or decrypt a file with AES + password",
        Fore.RESET + Style.BRIGHT + "2. IP Tracer Tool - trace info of any IP using ipinfo API",
        Fore.RESET + Style.BRIGHT + "3. Scanning Tool - scan open TCP ports in an IP address",
        "",
        Fore.YELLOW + Style.BRIGHT + "How to use this program:",
        Fore.RESET + Style.BRIGHT + "- Clone the repo: " + Fore.GREEN + "git clone https://github.com/Sown0205/Spryzen.git",
        Fore.RESET + Style.BRIGHT + "- Install required libraries: " + Fore.GREEN + "bash install.sh",
        Fore.RESET + Style.BRIGHT + "- Run it: " + Fore.GREEN + "python spryzen.py",
        "",
        Fore.YELLOW + Style.BRIGHT + "[!] Caution: Scanner tool in this program needs root access to run or it will raise PermissionError",
        Fore.GREEN + Style.BRIGHT + "[!] Solution: Use root access to run the program: " + Fore.GREEN + "sudo python spryzen.py",
        "",
        Fore.YELLOW + Style.BRIGHT + "Other information:",
        Fore.RESET + Style.BRIGHT +  "- This is a personal project for learning programming and cybersecurity.",
        "- It's not meant for real-world security use.",
        "- But you can play with it to understand how things work!",
        "- It's open source. Pull requests are welcome! Feel free to contribute",
        "",
        Fore.YELLOW + Style.BRIGHT + "Contact information:",
        Fore.RESET + "- Gmail: buithaison13579@gmail.com",
        "- Facebook: https://www.facebook.com/son.bui.5730",
        "- GitHub: https://github.com/Sown0205",
        "",
        Fore.CYAN + "Thank you for using this tool and reading this information :>" + Style.RESET_ALL
    ]
                  
    sleep(0.7) # add a little delay before displaying the msg
    utils.show_banner() # Show the banner first
    for line in lines:
        print(line) # Show about us info
    #Show again the menu
    utils.show_menu()
