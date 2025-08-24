#import colorama
from colorama import Fore, Style, init, Cursor
import sys
import os
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
                      Version: {Fore.YELLOW}v.1.2{Fore.CYAN}\n
------------------------------------------------------------------------------
"""
    print(Fore.CYAN + Style.BRIGHT + banner, end="")
    print(Fore.RESET, end="")

#Show menu 
def show_menu():
    print(Fore.RESET + Style.BRIGHT + r"""Use a tool from the menu list below, or choose 'About us' to see details 
about this program and how to use it""" + "\n")
    print(Fore.YELLOW + Style.BRIGHT + f"[1] Crypto tool (Encryption/Decryption)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[2] IP Tracer tool (trace IP addresses)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[3] Scanning Tool (Scanning for open ports)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[4] Hash Checker Tool (Password hash, verify hash)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[5] About us (info about this program)" )
    print(Fore.YELLOW + Style.BRIGHT + f"[0] Quit (Exit the program)\n" )
    print(Fore.CYAN + Style.BRIGHT + "------------------------------------------------------------------------------")

#Display goodbye message if users quit the program
def goodbye():
    print(Fore.RED + Style.BRIGHT + "Quitting...\n")
    sleep(2)
    print(Fore.CYAN + Style.BRIGHT + "Goodbye :) !")
    sys.exit()

# Function to clear only the dynamic output area
def clear_output_area():
    print("\033[17;0H\033[J", end="")  # Move to line 18 and clear down

#TODO: Enhancing clear_output_area function, as this is a out-of-dated and non-efficent technique
# The best solution to clear the output area is to actually clear all the UI in the terminal, then display again the banner

"""
import os

def exit_and_display():
    sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
"""

