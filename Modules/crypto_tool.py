# Cryptography Tool
# Required libraries: cryptography, colorama
# pip install cryptography colorama

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from colorama import init, Fore, Style
from time import sleep
init(autoreset=True)

#Import utils module to use reuseable code
from Modules import utils

# Function to generate a random AES-256 key size
def generate_key():
    key = os.urandom(32)  # Randomly generated AES-256 key size
    return key

# Function to encrypt the files by using the AES key
def encrypt_file():
    sleep(0.5)
    utils.clear_output_area()
    file_path = input("Enter the file path that you want to encrypt: \n")
    
    # Handle unknown files
    if not os.path.exists(file_path):
        print(Fore.RED + "File not found!")
        sleep(1.5)
        utils.clear_output_area()
        return
    
    #Prompt the user if they really want to encrypt the file
    else:
        utils.clear_output_area()
        prompt = input(Fore.YELLOW + Style.BRIGHT + "Do you really want to encrypt this file (yes/no ?): ")
        
        #if no - return
        if prompt == "no" or prompt == "n":
            print(Fore.YELLOW + Style.BRIGHT + "Make sure that you really want to encrypt this file. If the decryption key is lost, decryption will be impossible")
            sleep(2)
            utils.clear_output_area()
            return
        
        #if yes - continue
        elif prompt == "yes" or prompt == "y": 
            key = generate_key()
            
            # Encrypting
            f_input = open(file_path, "rb")
            data = f_input.read()
            f_input.close()

            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            encrypted_file_path = file_path + ".enc"
            f_output = open(encrypted_file_path, "wb")
            f_output.write(iv + ciphertext)
            f_output.close()
            
            os.remove(file_path) #remove the orginal filepath to erase track
            print(Fore.GREEN + Style.BRIGHT + f"\nYour file {file_path} has been encrypted and the original content has been deleted")
            print(Fore.GREEN + Style.BRIGHT + f"Your encrypted file: {encrypted_file_path}\n")
            print(Fore.GREEN + Style.BRIGHT + f"Encryption key (THIS IS IMPORTANT IF YOU WANT TO DECRYPT THE FILE ! SAVE IT): {key.hex()} \n")

            # Save the key into a file if users want to
            # Make a loop to validate user's choices
            while True:
                    save_option = input(Fore.YELLOW + Style.BRIGHT + "Do you want to save the key to a file? (yes/no): ").strip().lower()

                    #If choose 'yes' -> save the key to a file then break the loop
                    if save_option == "yes" or save_option == "y":
                    # Use a loop to make sure the user enter the valid key path
                        while True:
                            key_file = input("Enter the filename to save the key: ").strip()
                            #Check file path valid or not
                            if ".txt" not in key_file:
                                print(Fore.RED + Style.BRIGHT + "\nInvalid key file path ! The file path should have '.txt' extension")
                                print(Fore.RED + Style.BRIGHT + "Example: 'key.txt', 'secure.txt', 'lock.txt',...\n")
                                sleep(2)
                                utils.clear_output_area()
                                continue
                            
                            #The key file path should not be the same as the original file path
                            elif key_file == file_path:
                                print(Fore.RED + "The file path should not be the same as the original file path. Try a different name")
                                sleep(1.5)
                                utils.clear_output_area()
                                continue
                            else:
                                with open(key_file, "w") as f:
                                    f.write(key.hex())
                                print(Fore.GREEN + f"Key saved to {key_file}")
                                sleep(3)
                                utils.clear_output_area()
                                break
                        break

                    #if choose 'no' -> break the loop (nothing to do more)
                    elif save_option == "no" or save_option == "n":
                        print(Fore.YELLOW + Style.BRIGHT + "It is recommended that you should save the key to a file. If you lost the key, decryption is impossible")
                        sleep(1)
                        utils.clear_output_area()
                        break

                    #Else -> continue the loop to make sure users choose the right command
                    else: 
                        print(Fore.RED + "\nInvalid command. Choose 'yes' ('y') or 'no' ('n') \n")
                        sleep(1)
                        utils.clear_output_area()
                        continue

        # if other inputs are made - display invalid command and return
        else: 
            print(Fore.RED + "\nInvalid command ! Choose 'yes' ('y') or 'no' ('n')")
            sleep(1)
            utils.clear_output_area()
            return

# Function to decrypt the file with the provided key
def decrypt_file():
    sleep(0.5)
    utils.clear_output_area()
    encrypted_file_path = input("Enter the encrypted file path that you want to decrypt: ")

    #Handle unknown file paths
    if not os.path.exists(encrypted_file_path):
        print(Fore.RED + "File not found!")
        sleep(1.5)
        utils.clear_output_area()
        return
    
    # Handle invalid encrypted file
    file_extension = ".enc"
    if not encrypted_file_path.endswith(file_extension):
        print(Fore.RED + "Error: File is not a valid encrypted file.")
        sleep(1.5)
        utils.clear_output_area()
        return
    
    key_hex = input("Enter the decryption key: \n")

    # Key validations
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        print(Fore.RED + "Invalid key format!")
        sleep(1.5)
        utils.clear_output_area()
        return
    
    with open(encrypted_file_path, "rb") as f:
        data = f.read()
    
    iv = data[:16]
    ciphertext = data[16:]
    
    # Decrypting
    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
        
        decrypted_file_path = encrypted_file_path.replace(".enc", "")
        with open(decrypted_file_path, "wb") as f:
            f.write(plaintext)
        
        os.remove(encrypted_file_path) # Remove the encrypted file path as the file has been decrypted
        print(Fore.GREEN + f"Your file {encrypted_file_path} has been decrypted")
        print(Fore.GREEN + f"Decrypted file: {decrypted_file_path}")
        print(Fore.YELLOW + Style.BRIGHT + "Exitting...")
        sleep(4)
        utils.clear_output_area()

    # Error handling
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "Decryption failed: Invalid key!")

# Execute function
def run():
    print(Fore.CYAN + Style.BRIGHT + "[✓] Booting Cryptography Tool...")
    sleep(1)
    utils.clear_output_area()
    while True:
        print(Style.BRIGHT + "Choose your cryptography mode [1-2] or quit [3]\n")
        print(Fore.YELLOW + Style.BRIGHT + "[1] Encrypt mode")
        print(Fore.YELLOW + Style.BRIGHT + "[2] Decrypt mode")
        print(Fore.YELLOW + Style.BRIGHT + "[3] Quit \n")

        choice = input(Fore.CYAN + Style.BRIGHT + "Your choice: ").lower().strip()

        if choice == "1":
            encrypt_file()

        elif choice == "2":
            decrypt_file()

        elif choice == "3":
            print(Fore.RED + Style.BRIGHT + "Quitting...\n")
            sleep(1)
            utils.clear_output_area()
            utils.show_menu()
            break

        else:
            print(Fore.RED + Style.BRIGHT + "Invalid command !")
            utils.clear_output_area()
            continue
        
    