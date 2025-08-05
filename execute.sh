# this script is used to set up shortcut symbolic link to the program
# For example, to run the program, the command will be 
# python spryzen.py or sudo python spryzen.py
# However with this script, user can just run spryzen or sudo spryzen to execute the program, 
# and they can run the tool in anywhere rather than in just Spryzen folder

echo "[+] Creating spryzen command shortcut..."

#Requires root access to run
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run as root: sudo ./execute.sh${NC}"
    exit 1      
else
    ln -sf "$(pwd)/spryzen.py" /usr/local/bin/spryzen  
fi

echo "Now you can run the tool in anywhere with this command: spryzen - or sudo spryzen"




