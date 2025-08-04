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
    file_path = input("Enter the file that you want to encrypt: \n")
    
    # Handle unknown files
    if not os.path.exists(file_path):
        print(Fore.RED + "File not found!")
        return
    
    #Prompt the user if they really want to encrypt the file
    else:
        prompt = input(Fore.YELLOW + "Do you really want to encrypt this file (yes/no ?): ")
        
        #if no - return
        if prompt == "no" or prompt == "n":
            print(Fore.YELLOW + "Make sure that you really want to encrypt this file. If the decryption key is lost, decryption will be impossible")
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
            print(Fore.GREEN + f"\nYour file {file_path} has been encrypted and the original content has been deleted")
            print(Fore.GREEN + f"Your encrypted file: {encrypted_file_path}\n")
            print(Fore.GREEN + Style.BRIGHT + f"Encryption key (THIS IS IMPORTANT IF YOU WANT TO DECRYPT THE FILE ! SAVE IT): {key.hex()} \n")

            # Save the key into a file if users want to
            # Make a loop to validate user's choices
            while True:
                    save_option = input(Fore.YELLOW + "Do you want to save the key to a file? (yes/no): ").strip().lower()

                    #If choose 'yes' -> save the key to a file then break the loop
                    if save_option == "yes" or save_option == "y":
                    # Use a loop to make sure the user enter the valid key path
                        while True:
                            key_file = input("Enter the filename to save the key: ").strip()
                            #Check file path valid or not
                            if ".txt" not in key_file:
                                print(Fore.RED + "\nInvalid key file path ! The file path should have '.txt' extension")
                                print(Fore.RED + "Example: 'key.txt', 'secure.txt', 'lock.txt',...\n")
                                continue
                            
                            #The key file path should not be the same as the original file path
                            elif key_file == file_path:
                                print(Fore.RED + "The file path should not be the same as the original file path. Try a different name")
                                continue
                            else:
                                with open(key_file, "w") as f:
                                    f.write(key.hex())
                                print(Fore.GREEN + f"Key saved to {key_file}")
                                break
                        break

                    #if choose 'no' -> break the loop (nothing to do more)
                    elif save_option == "no" or save_option == "n":
                        break

                    #Else -> continue the loop to make sure users choose the right command
                    else: 
                        print(Fore.RED + "\nInvalid command. Choose 'yes' ('y') or 'no' ('n') \n")
                        continue

        # if other inputs are made - display invalid command and return
        else: 
            print(Fore.RED + "\nInvalid command ! Choose 'yes' ('y') or 'no' ('n')")
            return

# Function to decrypt the file with the provided key
def decrypt_file():
    encrypted_file_path = input("Enter the encrypted file that you want to decrypt: ")

    #Handle unknown file paths
    if not os.path.exists(encrypted_file_path):
        print(Fore.RED + "File not found!")
        return
    
    # Handle invalid encrypted file
    file_extension = ".enc"
    if not encrypted_file_path.endswith(file_extension):
        print(Fore.RED + "Error: File is not a valid encrypted file.")
        return
    
    key_hex = input("Enter the decryption key: \n")

    # Key validations
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        print(Fore.RED + "Invalid key format!")
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

    # Error handling
    except Exception as e:
        print(Fore.RED + "Decryption failed: Invalid key!")

# Execute function
def run():
    print(Fore.CYAN + Style.BRIGHT + "\n----------------------------------Using Cryptography Tool--------------------------------------------")
    while True:
        choice = input(Fore.CYAN + Style.BRIGHT + "\nChoose a crytography mode (encrypt or decrypt) or type quit to exit the program: ").lower().strip()
        if choice == "encrypt":
            encrypt_file()

        elif choice == "decrypt":
            decrypt_file()

        elif choice == "quit":
            print(Fore.CYAN + Style.BRIGHT + "Quitting...")
            sleep(1)
            utils.show_menu()
            break

        else:
            print(Fore.RED + Style.BRIGHT + "Invalid command. Choose 'encrypt/decrypt' or 'quit'")
            continue
        
    