#import colorama
from colorama import Fore, Style, init, Cursor
import sys
from time import sleep
init(autoreset=True)

# Utils module - contains re-useable code in the program

#Showing the banner
def show_banner():
    banner = f"""

  ██████  ██▓███   ██▀███ ▓██   ██▓▒███████▒▓█████  ███▄    █ 
▒██    ▒ ▓██░  ██▒▓██ ▒ ██▒▒██  ██▒▒ ▒ ▒ ▄▀░▓█   ▀  ██ ▀█   █ 
░ ▓██▄   ▓██░ ██▓▒▓██ ░▄█ ▒ ▒██ ██░░ ▒ ▄▀▒░ ▒███   ▓██  ▀█ ██▒
  ▒   ██▒▒██▄█▓▒ ▒▒██▀▀█▄   ░ ▐██▓░  ▄▀▒   ░▒▓█  ▄ ▓██▒  ▐▌██▒
▒██████▒▒▒██▒ ░  ░░██▓ ▒██▒ ░ ██▒▓░▒███████▒░▒████▒▒██░   ▓██░
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒▓ ░▒▓░  ██▒▒▒ ░▒▒ ▓░▒░▒░░ ▒░ ░░ ▒░   ▒ ▒ 
░ ░▒  ░ ░░▒ ░       ░▒ ░ ▒░▓██ ░▒░ ░░▒ ▒ ░ ▒ ░ ░  ░░ ░░   ░ ▒░
░  ░  ░  ░░         ░░   ░ ▒ ▒ ░░  ░ ░ ░ ░ ░   ░      ░   ░ ░ 
      ░              ░     ░ ░       ░ ░       ░  ░         ░ 
                           ░ ░     ░            
                                         
           Spryzen - A simple cyber toolkit written in Python
                      Author: {Fore.YELLOW}Sown0205{Fore.CYAN}
                      Version: {Fore.YELLOW}v.1.1{Fore.CYAN}
"""
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.RESET)

#Show menu 
def show_menu():
    print(Fore.CYAN + Style.BRIGHT + "------------------------------------------------------------------------------")
    print(Fore.RESET + Style.BRIGHT + r"""Use a tool from the menu list below, or choose 'About us' to see details about
this program and how to use it""" + "\n")
    print(Fore.YELLOW + Style.BRIGHT + f"[1] Crypto tool (Encryption/Decryption)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[2] IP Tracer tool (trace IP addresses)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[3] Scanning Tool (Scanning for open ports)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[4] About us (info about this program)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[0] Quit (Exit the program)\n" )
    print(Fore.CYAN + Style.BRIGHT + "------------------------------------------------------------------------------")

#Display goodbye message if users quit the program
def goodbye():
    print(Fore.RED + Style.BRIGHT + "Quitting...\n")
    sleep(2)
    print(Fore.CYAN + Style.BRIGHT + "Goodbye :) !")
    print(Fore.CYAN + Style.BRIGHT + "------------------------------------------------------------------------------")
    sys.exit()
