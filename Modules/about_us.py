from colorama import Fore, Style
from time import sleep
import os

#import utils module
from Modules import utils

# Main funtion
def run():
    lines = [
        Fore.YELLOW + Style.BRIGHT + "***[!] What's new:***",
        Fore.RESET + Style.BRIGHT + "The new version v.1.1 has some new features:",
        Fore.RESET + Style.BRIGHT + "1. Version checker: If the program is outdated, it will prompt the user to update to the current version",
        Fore.RESET + Style.BRIGHT + "2. Auto-update function: The program will also updates the current version automatically for the user without manual git commands",
        "",
        Fore.YELLOW + Style.BRIGHT + "[!] Caution: This feature is on testing and may cause some bugs. We recommend you not use this feature until later versions",
        "",
        Fore.RESET + Style.BRIGHT + "3. Enhanced UI display: The banner and menu will be static, only the output will be dynamically displayed",
        "",
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
    for line in lines:
        print(line) # Show about us info
    
    #Prompt the user to get back to the menu
    input(Fore.RESET + Style.BRIGHT + "\nPress any word to get back to the menu: ")
    # This is tricky - I haven't found any solution to clear the about us section without touching the banner and the menu
    # So the best way to do is to clear them all and display the banner and menu again :)
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(2)
    utils.show_banner()
    utils.show_menu()

