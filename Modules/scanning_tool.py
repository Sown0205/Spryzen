# Required libraries
# threading, scapy, re

import time
import threading
from scapy.all import IP, TCP, sr1, send
from colorama import Fore, Style, init
import re
init(autoreset=True)

#Import utils modulde to use reusable code
import utils

# Function to validate IP address
def is_valid_ip(ip_add):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if re.match(pattern, ip_add):
       return all(0 <= int(octet) <= 255 for octet in ip_add.split("."))
    return False

# Function to validate port number
def is_valid_port(port):
    return isinstance(port, int) and 1 <= port <= 65535

#Function to SYN scan on a single port
def syn_scan(target, port, results):
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

#Muilti-threading to scan multiple ports
def scan_ports(target, ports):
    threads = []
    results = []  # Store open/closed ports

    for port in ports:
        t = threading.Thread(target=syn_scan, args=(target, port, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Display message if no open/closed ports found
    if not results:
        print(Fore.YELLOW + Style.BRIGHT + "\n[!] No open or closed ports found in the given range.")

#Execute function
def run():
    print(Fore.CYAN + Style.BRIGHT + "\n----------------------------------Using Port Scanning Tool--------------------------------------------")
    
    while True:
        ip_address = input(Fore.CYAN + Style.BRIGHT + "Enter you IP address here to type 'quit' to exit the program: ")

        if ip_address == "quit":
            print(Fore.CYAN + Style.BRIGHT + "Quitting...")
            time.sleep(1)
            utils.show_menu()
            break

        else:
            if not is_valid_ip(ip_address):
                print(Fore.RED + Style.BRIGHT + "Invalid IP address !")
                continue

            else: 
                prompt= input(Fore.CYAN + Style.BRIGHT + "Do you want to scan port/ports or port range ? Type 'ports' for port/ports scan or type 'range' or port range scan: ").strip().lower()

                if prompt == "ports":
                    print(Fore.CYAN + Style.BRIGHT + "Specify your port/ports here. If you want to scan multiple ports, seperate each port by a comma (,)")
                    print("Example: 80 or 135,139,445")
                    ports = input(Fore.CYAN + Style.BRIGHT + "Enter your port/ports: ")

                    for port in ports.split(","):
                        port = port.strip()
                        if not port.isdigit(): #Check if port is numeric
                            print(Fore.RED + Style.BRIGHT + f"Invalid port {port} ! Ports value must be a number")
                            continue

                elif prompt == "range":
                    ajfefnefn

                else:
                    print(Fore.RED + Style.BRIGHT + "Invalid command !")
                    continue

        



