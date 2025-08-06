# Required libraries
# threading, scapy, re

import time
import threading
from scapy.all import IP, TCP, sr1, send
from colorama import Fore, Style, init
import re
from datetime import datetime
init(autoreset=True)

#Import utils modulde to use reusable code
from Modules import utils

# Function to validate IP address
def is_valid_ip(ip_add):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if re.match(pattern, ip_add):
       return all(0 <= int(octet) <= 255 for octet in ip_add.split("."))
    return False

# Function to validate port number
def is_valid_port(port):
    return isinstance(port, int) and 1 <= port <= 65535

# Shared error container
scan_error = None
scan_error_lock = threading.Lock()

#Function to SYN scan on a single port
def syn_scan(target, port, results):
    global scan_error
    #Put the scan in a try-except block to catch any errors
    try:
        pkt = IP(dst=target) / TCP(dport=port, flags="S")  # SYN Packet
        response = sr1(pkt, timeout=1, verbose=0)  # Send & receive response

        if response:
            if response.haslayer(TCP):
                if response[TCP].flags == 0x12:  # SYN-ACK received
                    print(Fore.GREEN + Style.BRIGHT + f"[+] Port {port} is OPEN")
                    send(IP(dst=target) / TCP(dport=port, flags="R"), verbose=0)  # Send RST to close
                    results.append(port)
                elif response[TCP].flags == 0x14:  # RST-ACK received
                    print(Fore.RED + Style.BRIGHT + f"[-] Port {port} is CLOSED")
                    results.append(port)

    except Exception as e:
        # Thread-safe error storage
        with scan_error_lock:
            if scan_error is None:
                scan_error = e

#Muilti-threading to scan multiple ports
def scan_ports(target, ports):

    global scan_error
    threads = []
    results = []  # Store open/closed ports

    for port in ports:
        t = threading.Thread(target=syn_scan, args=(target, port, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if scan_error is not None:
        # If error occurred, print message and skip results
        print(Fore.RED + Style.BRIGHT + f"\n[!] Scan aborted ! Error: {scan_error}")
        print(Fore.RED + Style.BRIGHT + "Exitting the program...")
        return False, results
    
    # Display message if no open/closed ports found
    elif not results:
        print(Fore.YELLOW + Style.BRIGHT + "\n[!] No open or closed ports found in the given range.")
    
    return True, results

#Execute function
def run():
    print(Fore.CYAN + Style.BRIGHT + "[✓] Booting Scanning Tool...\n")
    time.sleep(1)
    utils.clear_output_area()
 
    while True:
        ip_address = input(Fore.RESET + Style.BRIGHT + "Enter your IP address here: ")

        if not ip_address:
            print(Fore.YELLOW + Style.BRIGHT + "IP address missing. Please provide a IP address")
            time.sleep(1)
            utils.clear_output_area()
            continue

        elif not is_valid_ip(ip_address):
            print(Fore.RED + Style.BRIGHT + "Invalid IP address !")
            time.sleep(1)
            utils.clear_output_area()
            continue

        else: 
            prompt= input(Fore.CYAN + Style.BRIGHT + "Type 'ports' for port/ports scan or 'range' for port range scan: ").strip().lower()

            if prompt == "ports":
                while True:
                    time.sleep(1.5)
                    utils.clear_output_area()
                    print(Fore.CYAN + Style.BRIGHT + "Specify your port/ports here. If you want to scan multiple ports, seperate each port by a comma (,)")
                    print("Example: 80 or 135,139,445\n")

                    ports = input(Fore.CYAN + Style.BRIGHT + "Enter your port/ports: ")
                    port_list = []
                    error = False

                    for port in ports.split(","):
                        port = port.strip()
                        if not port.isdigit(): #Check if port is numeric
                            print(Fore.RED + Style.BRIGHT + f"Invalid port {port} ! Ports value must be a number")
                            error = True
                            break

                        port = int(port)
                        if not is_valid_port(port):
                            print(Fore.RED + Style.BRIGHT + "Invalid port value ! Port value must be between 1-65535")
                            error = True
                            break

                        port_list.append(port)
                    
                    if error or not port_list:
                        time.sleep(1)
                        utils.clear_output_area()
                        continue
                    break

            elif prompt == "range":
                while True:
                    time.sleep(1.5)
                    utils.clear_output_area()
                    print(Fore.CYAN + Style.BRIGHT + "Specify your port range here. Caution: start port and end port must be seperated by a hyphen (-)")
                    print("Example: 1-1000 or 100-500")

                    port_range = input(Fore.CYAN + Style.BRIGHT + "Enter your port range: ")

                    if "-" not in port_range:
                        print(Fore.RED + Style.BRIGHT + "Invalid range format. Start port and end port must be seperated by a hyphen (-)")
                        time.sleep(1)
                        utils.clear_output_area()
                        continue

                    start, end = port_range.split("-")

                    if not start.strip().isdigit() or not end.strip().isdigit():
                        print(Fore.RED + Style.BRIGHT + "Start and end port values must be numbers.")
                        time.sleep(1)
                        utils.clear_output_area()
                        continue
                    
                    start = int(start.strip())
                    end = int(end.strip())

                    if not is_valid_port(start) or not is_valid_port(end):
                        print(Fore.RED + Style.BRIGHT + "Start port and end port must be in range from 1-65536")
                        time.sleep(1)
                        utils.clear_output_area()
                        continue

                    if start > end: 
                        print(Fore.RED + Style.BRIGHT + "Start port must be smaller than end port") 
                        time.sleep(1)
                        utils.clear_output_area()
                        continue

                    else:
                        port_list = []
                        port_list = list(range(start, end + 1))    
                        break               

            else:
                print(Fore.RED + Style.BRIGHT + "Invalid command !")
                time.sleep(1.5)
                utils.clear_output_area()
                continue

            print(Fore.RESET + Style.BRIGHT + f"\nStarting SYN scan on {Fore.YELLOW}{Style.BRIGHT}{ip_address} {Fore.RESET}{Style.RESET_ALL} at {Style.BRIGHT}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            #Time counter
            start_time = time.time()
            success, results = scan_ports(ip_address, port_list)
            end_time = time.time()

            if success:           
                print(Fore.RESET + Style.BRIGHT + f"\nScan completed ! IP address {Fore.YELLOW}{Style.BRIGHT}{ip_address} {Fore.RESET}{Style.RESET_ALL} scanned in {Fore.YELLOW}{Style.BRIGHT}{round(end_time - start_time, 2)} seconds.")
                #Prompt user if they want to continue or not
                user_prompt = input(Fore.YELLOW + Style.BRIGHT + "Do you want to continue (yes/no): ").strip().lower()

                if user_prompt == "yes":
                    time.sleep(1.5)
                    utils.clear_output_area()
                    continue

                elif user_prompt == "no":
                    print(Fore.RED + Style.BRIGHT + "Quitting...\n")
                    time.sleep(1.5)
                    utils.clear_output_area()
                    utils.show_menu()
                    break
                # If invalid choice, exit the tool anyway but display a warning msg
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "Invalid command ! Exiting the tool...")
                    time.sleep(1.5)
                    utils.clear_output_area()
                    utils.show_menu()
                    break
            # If encoutering scan error, clear this and break
            else:
                time.sleep(1.5)
                utils.clear_output_area()
                utils.show_menu()
                break


