#!/usr/bin/env python3
# Make spryzen.py has a proper shebang at the top so it wont be misunderstood as a bash file
# Required libraries
import sys
from time import sleep
from colorama import Fore, Style, init
init(autoreset=True)

#Collecting tools and modules for the program
from Modules import crypto_tool
from Modules import ip_tracer
from Modules import scanning_tool
from Modules import about_us
from Modules import utils
from Modules import updater

# Main function
def main():
    #Checking for updates
    updater.check_update()
    utils.show_banner() #Show banner
    utils.show_menu() #Show menu list
    while True:
        user_choice = input(Fore.RESET + Style.BRIGHT + "Select your choice [1-5] to use the program or choose 0 to quit: ")
        print(Fore.RESET) #Reset the text color
        
        if user_choice == "1":
            crypto_tool.run() # Run the first tool

        elif user_choice == "2":
            ip_tracer.run() # Run the second tool

        elif user_choice == "3":
            scanning_tool.run() # Run the third tool

        elif user_choice == "4":
            about_us.run() # Display about us info

        elif user_choice == "0":
            utils.goodbye() # exit the program

        # If invalid choice, display error and prompt the user to choose again
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid choice ! Choose again\n")
            continue

if __name__ == "__main__":
    main()