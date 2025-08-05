#Spryzen installer script
# This is the script to setup Spryzen on a newly Linux box. You can install all the requirements manually,
# Or you can run this bash file: bash install.sh
# Or sudo chmod +x install.sh --> install.sh

#------------------------Script---------------------------------------
# Color Codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color (reset)

# Detect package manager
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
    INSTALL_CMD="apt install -y"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
    INSTALL_CMD="yum install -y"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
    INSTALL_CMD="dnf install -y"
elif command -v pacman &> /dev/null; then
    PKG_MANAGER="pacman"
    INSTALL_CMD="pacman -S --noconfirm"
elif command -v apk &> /dev/null; then
    PKG_MANAGER="apk"
    INSTALL_CMD="apk add"
else
    echo -e "${RED}[!] Caution ! No supported package manager found. Exiting..."
    exit 1
fi

echo "Your Linux distro is using package manager: ${PKG_MANAGER}. Procedding..."

#Header message
echo -e "${BLUE}${BOLD} Spryzen Installer - Starting setup...${NC}"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Please run as root: sudo ./install.sh${NC}"
  exit 1
fi

echo "${YELLOW} [+] Updating package lists and upgrading system...${NC}"

case $PKG_MANAGER in
  apt)
    sudo apt update && $SUDO apt upgrade -y
    ;;
  yum)
    $SUDO yum update -y
    ;;
  dnf)
    $SUDO dnf upgrade --refresh -y
    ;;
  pacman)
    $SUDO pacman -Syu --noconfirm
    ;;
  apk)
    $SUDO apk update && $SUDO apk upgrade
    ;;
  *)
    echo "[!] Unknown package manager: $PKG_MANAGER"
    exit 1
    ;;
esac

# Install Python3 and pip if not found
echo "${GREEN}[+] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[!] Python3 not found. Installing..."
    $INSTALL_CMD python3
else 
    echo -e "${GREEN}[+] Python3 already installed."
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[!] pip3 not found. Installing...${NC}"
    $INSTALL_CMD python3-pip
else 
    echo -e "${GREEN}[+] pip3 already installed."
fi

# Install git and curl
$INSTALL_CMD git curl

#Installing required Python libraries for the program
echo -e "${YELLOW}[+] Installing required Python libraries...${NC}"
pip install --upgrade pip
pip install argparse cryptography colorama requests scapy

#Make spryzen.py executable
sudo chmod +x spryzen.py

#Complete
echo -e "${GREEN}[+] Installation complete !"
echo "You can now run the program using this command: ${YELLOW}spryzen.py${NC} or ${YELLOW}sudo spryzen.py${NC}"




