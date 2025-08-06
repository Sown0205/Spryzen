#Required libraries: requests, argparse, colorama
import requests
from colorama import Fore, Style, init
init(autoreset=True)
import re
from time import sleep

#import utils - using reusable code 
from Modules import utils

#Trace IP function
def trace_ip(ip_address):
    try: 
        # Send the request to ipinfo API
        request_url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(request_url)

        #If receive response (status code 200 OK), display its contents
        if response.status_code == 200:
            ip_data = response.json()
            print(Fore.CYAN + Style.BRIGHT + f"IP address information for: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('ip', 'N/A')}")
            print(Fore.CYAN + f"-" * 40)
            print(Fore.CYAN + f"IP address: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('ip', 'N/A')}")
            print(Fore.CYAN + f"Hostname: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('hostname', 'N/A')}")
            print(Fore.CYAN + f"Country: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('country', 'N/A')}")
            print(Fore.CYAN + f"Region: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('region', 'N/A')}")
            print(Fore.CYAN + f"City: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('city', 'N/A')}")
            print(Fore.CYAN + f"Location (Latitude and Longnitude): " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('loc', 'N/A')}")
            print(Fore.CYAN + f"Organizations: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('org', 'N/A')}")
            print(Fore.CYAN + f"Postal: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('postal', 'N/A')}")
            print(Fore.CYAN + f"Timezone: " + Fore.YELLOW + Style.BRIGHT + f"{ip_data.get('timezone', 'N/A')}")
            print(Fore.CYAN + f"-" * 40)

        # If not recevice response (status code != 200), display error
        else:
            error = response.json()
            print(Fore.RED + f"Cannot find info for IP address {ip_address}. Response status code: {response.status_code}")
            print(Fore.RED + Style.BRIGHT + f"Error: {error.get('title')}")
            print(Fore.RED + Style.BRIGHT + f"{error.get('message')}")

    # Exceptions
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + "Request failed !")
        print(Fore.RED + Style.BRIGHT + f"Error: {e}")

#Validate IP address
def is_valid_ip(ip):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if re.match(pattern, ip):
       return all(0 <= int(octet) <= 255 for octet in ip.split("."))
    return False

#Execute function
def run():
    print(Fore.CYAN + Style.BRIGHT + "[✓] Booting IP Tracer Tool...\n")
    sleep(0.5)
    
    while True:
        ip_add = input(Fore.CYAN + Style.BRIGHT + "Enter an IP address (leave blank for your own IP): ").strip()
        if not ip_add:
            ip_add = ""
            trace_ip(ip_add)
        
        else:
            if is_valid_ip(ip_add):
                trace_ip(ip_add)
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid IP address !")
                break
            
        prompt = input(Fore.CYAN + Style.BRIGHT + "Do you want to continue ? (yes/no): ").lower().strip()
    
        if prompt == "yes":
            continue
        elif prompt == "no":
            print(Fore.CYAN + Style.BRIGHT + "Quitting...")
            sleep(0.5)
            utils.show_menu()
            break
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Invalid choice ! Choose 'yes' or 'no'")
            utils.show_menu()
            break
            
