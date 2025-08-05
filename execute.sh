#!/usr/bin/env python3

# this script is used to set up shortcut symbolic link to the program
# For example, to run the program, the command will be 
# python spryzen.py or sudo python spryzen.py
# However with this script, user can just run spryzen or sudo spryzen to execute the program, 
# and they can run the tool in anywhere rather than in just Spryzen folder

#Color Codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color (reset)

echo -e "${GREEN}[+] Creating spryzen command shortcut...${NC}"

#Make sryzen.py executable first
sudo chmod +x spryzen.py

#Requires root access to run
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: Permission denied ! Please run as root: sudo ./execute.sh${NC}"
    exit 1      
else
    ln -sf "$(pwd)/spryzen.py" /usr/local/bin/spryzen  
fi

echo -e "Now you can run the tool in anywhere with this command: ${YELLOW}spryzen${NC} - or ${YELLOW}sudo spryzen${NC}"




