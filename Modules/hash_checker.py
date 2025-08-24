# New module tool - Password hash checker
# Support bcrypt, scrypt, argon2
# Required libraries: bcrypt, scrypt, argon2-cffi
# pip install bcrypt scrypt argon2-cffi

import bcrypt
import hashlib
import os
import scrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from colorama import Fore, Style, init
from time import sleep
init(autoreset=True)
#Reusable code
from Modules import utils

#----------------------Bcrypt hash and verify --------------------------------- #

def bcrypt_hash(password: str, rounds: int = 12) -> str:
    """
    Hash password using bcrypt
    rounds: cost factor (4-31, default 12)
    Higher rounds = more secure but slower
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def bcrypt_verify(password: str, hashed: str) -> bool:
    """Verify password against bcrypt hash"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# ------------------------ Argon2 hash and verify --------------------------------------- #

def argon2_hash(password: str, time_cost: int = 2, memory_cost: int = 65536, parallelism: int = 1) -> str:
    """
    Hash password using Argon2id
    time_cost: number of iterations
    memory_cost: memory usage in KiB
    parallelism: number of parallel threads
    """
    ph = PasswordHasher(
        time_cost=time_cost,      # 2 iterations
        memory_cost=memory_cost,  # 64 MB
        parallelism=parallelism   # 1 thread
    )
    return ph.hash(password)

def argon2_verify(password: str, hashed: str) -> bool:
    """Verify password against Argon2 hash"""
    ph = PasswordHasher()
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False
    
# --------------------------- Scrypt hash and verify ------------------------------------------------- #

def scrypt_hash(password: str, N: int = 16384, r: int = 8, p: int = 1, key_len: int = 32) -> str:
    """
    Hash password using scrypt
    N: CPU/memory cost parameter (power of 2)
    r: block size parameter
    p: parallelization parameter
    key_len: derived key length
    """
    salt = os.urandom(32)  # 32 bytes salt
    key = scrypt.hash(password.encode('utf-8'), salt, N, r, p, key_len)
    
    # Store salt and hash together (custom format)
    import base64
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    key_b64 = base64.b64encode(key).decode('utf-8')
    return f"$scrypt$N={N},r={r},p={p}${salt_b64}${key_b64}"
    
def scrypt_verify(password: str, stored_hash: str) -> bool:
    """Verify password against scrypt hash"""
    try:
        import base64
        parts = stored_hash.split('$')
        if len(parts) != 4 or parts[0] != '' or parts[1] != 'scrypt':
            return False
        
        # Parse parameters
        params = {}
        for param in parts[2].split(','):
            key, value = param.split('=')
            params[key] = int(value)
        
        salt = base64.b64decode(parts[3])
        stored_key = base64.b64decode(parts[4])
        
        # Hash the input password with same parameters
        key = scrypt.hash(
            password.encode('utf-8'), 
            salt, 
            params['N'], 
            params['r'], 
            params['p'], 
            len(stored_key)
        )
        
        return key == stored_key
    except:
        return False
    
# ----------------------------- PBKDF2 hash and verify ---------------------------------------- #
def pbkdf2_hash(password: str, iterations: int = 100000, key_len: int = 32, algorithm: str = '') -> str:
    """
    Hash password using PBKDF2
    iterations: number of iterations (100,000+ recommended)
    key_len: derived key length in bytes
    algorithm: hash algorithm ('sha256', 'sha512')
    """
    salt = os.urandom(32)  # 32 bytes salt
    
    if algorithm == 'sha256':
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, key_len)
    elif algorithm == 'sha512':
        key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, iterations, key_len)
    else:
        raise ValueError("Unsupported algorithm")
    
    # Store in custom format
    import base64
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    key_b64 = base64.b64encode(key).decode('utf-8')
    return f"$pbkdf2-{algorithm}${iterations}${salt_b64}${key_b64}"
    
def pbkdf2_verify(password: str, stored_hash: str) -> bool:
    """Verify password against PBKDF2 hash"""
    try:
        import base64
        parts = stored_hash.split('$')
        if len(parts) != 4:
            return False
        
        algorithm = parts[1].replace('pbkdf2-', '')
        iterations = int(parts[2])
        salt = base64.b64decode(parts[3])
        stored_key = base64.b64decode(parts[4])
        
        # Hash the input password with same parameters
        key = hashlib.pbkdf2_hmac(
            algorithm, 
            password.encode('utf-8'), 
            salt, 
            iterations, 
            len(stored_key)
        )
        
        return key == stored_key
    except:
        return False
    
# --------------------------------------- Execute function (called on 'spryzen.py' later) ------------------------------------ #
def exec():
    print(Fore.CYAN + Style.BRIGHT + f"[✓] Booting Hash Checker Tool...")
    sleep(1)
    utils.clear_output_area()
    while True:
        print(Style.BRIGHT + "Select your choice [1-3]\n")
        print(Fore.YELLOW + Style.BRIGHT + "[1] Hash your password")
        print(Fore.YELLOW + Style.BRIGHT + "[2] Verify hash")
        print(Fore.YELLOW + Style.BRIGHT + "[3] Exit\n")
        choice = input("Your choice: ")

        if choice == "1":
            while True: 
                sleep(1)
                utils.clear_output_area()
                print(Style.BRIGHT + "Select your hash type [1-4]\n")
                print(Fore.YELLOW + Style.BRIGHT + "[1] Bcrypt hash (12 rounds)")
                print(Fore.YELLOW + Style.BRIGHT + "[2] Argon2 hash (2 iterations, 64 Mib memory usage)")
                print(Fore.YELLOW + Style.BRIGHT + "[3] Scrypt hash (32-bit derived key length (salt))")
                print(Fore.YELLOW + Style.BRIGHT + "[4] PBKDF2 hash (100.000+ iterations, support SHA-256 and SHA-512 algorithm)\n")

                choice = input("Your choice: ")
                if choice == "1":
                    sleep(1)
                    utils.clear_output_area()

                    password = input("Enter your password: ")
                    hashed_password = bcrypt_hash(password)
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour hashed password (bcrypt): " + Fore.RESET + hashed_password)

                    prompt = input("Continue ? (yes/no): ").strip().lower()

                    if prompt == "yes":
                        utils.clear_output_area()
                        continue
                    elif prompt == "no":
                        utils.clear_output_area()
                        break
                    else: 
                        print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                        utils.clear_output_area()
                        break
                    
                elif choice == "2":
                    sleep(1)
                    utils.clear_output_area()

                    password = input("Enter your password: ")
                    hashed_password = argon2_hash(password)
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour hashed password (argon2): " + Fore.RESET + hashed_password)

                    prompt = input("Continue ? (yes/no): ").strip().lower()

                    if prompt == "yes":
                        utils.clear_output_area()
                        continue
                    elif prompt == "no":
                        sleep(1)
                        utils.clear_output_area()
                        break
                    else: 
                        print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                        utils.clear_output_area()
                        break

                elif choice == "3":
                    sleep(1)
                    utils.clear_output_area()

                    password = input("Enter your password: ")
                    hashed_password = scrypt_hash(password)
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour hashed password (scrypt): " + Fore.RESET + hashed_password)

                    prompt = input("Continue ? (yes/no): ").strip().lower()

                    if prompt == "yes":
                        utils.clear_output_area()
                        continue
                    elif prompt == "no":
                        sleep(1)
                        utils.clear_output_area()
                        break
                    else: 
                        print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                        utils.clear_output_area()
                        break

                elif choice == "4":
                    sleep(1)
                    utils.clear_output_area()

                    print(Style.BRIGHT + "Choose hash algorithm\n")
                    print(Fore.YELLOW + Style.BRIGHT + "[1] SHA-256")
                    print(Fore.YELLOW + Style.BRIGHT + "[2] SHA-512\n")

                    mode = input("Your choice: ")
                    if mode == "1":
                        sleep(1)
                        utils.clear_output_area()

                        algorithm = "sha256"
                        password = input("Enter your password: ")
                        hashed_password = pbkdf2_hash(password, algorithm=algorithm)
                        print(Fore.YELLOW + Style.BRIGHT + f"\nYour hashed password (pbkdf2, {algorithm}): " + Fore.RESET + hashed_password)

                        prompt = input("Continue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            sleep(1)
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break
                    
                    elif mode == "2":
                        sleep(1)
                        utils.clear_output_area()

                        algorithm = "sha512"
                        password = input("Enter your password: ")
                        hashed_password = pbkdf2_hash(password, algorithm=algorithm)
                        print(Fore.YELLOW + Style.BRIGHT + f"\nYour hashed password (pbkdf2, {algorithm}): " + Fore.RESET + hashed_password)

                        prompt = input("Continue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            sleep(1)
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            sleep(1)
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            sleep(1)
                            utils.clear_output_area()
                            break

                    else:
                        print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                        sleep(1)
                        utils.clear_output_area()
                        break

                else:
                    print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                    continue

        elif choice == "2":
            while True:
                sleep(1)
                utils.clear_output_area()
                hashed_text = input(Style.BRIGHT + "Enter your hashed text here: \n")
                # Checking for hash headers:
                # Bcrypt header
                if "$2b$12$" in hashed_text:
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour text was hashed in bcrypt hash")
                    plain_text = input(Style.BRIGHT + "Enter your plain text: ")

                    verify = bcrypt_verify(password=plain_text, hashed=hashed_text)
                    if (verify):
                        print(Fore.GREEN + Style.BRIGHT + "\n[✓] Plain text match exacts with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break
                    else:
                        print(Fore.RED + Style.BRIGHT + "\n[X] Plain text does not match with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break

                #Argon2 header
                elif "$argon2id$v=19$m=65536,t=2,p=1" in hashed_text:
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour text was hashed in argon2 hash")
                    plain_text = input(Style.BRIGHT + "Enter your plain text: ")

                    verify = argon2_verify(password=plain_text, hashed=hashed_text)
                    if (verify):
                        print(Fore.GREEN + Style.BRIGHT + "\n[✓] Plain text match exacts with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break
                    else:
                        print(Fore.RED + Style.BRIGHT + "\n[X] Plain text does not match with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break

                #Scrypt header
                elif "$scrypt$N=16384,r=8,p=1$" in hashed_text:
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour text was hashed in Scrypt hash")
                    plain_text = input(Style.BRIGHT + "Enter your plain text: ")

                    verify = scrypt_verify(password=plain_text, stored_hash=hashed_text)
                    if (verify):
                        print(Fore.GREEN + Style.BRIGHT + "\n[✓] Plain text match exacts with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break
                    else:
                        print(Fore.RED + Style.BRIGHT + "\n[X] Plain text does not match with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break

                #pbkdf2 with sha-256 header
                elif "$pbkdf2-sha256$100000$" in hashed_text:
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour text was hashed in Pbkdf2 hash with SHA-256 hash algorithm")
                    plain_text = input(Style.BRIGHT + "Enter your plain text: ")

                    verify = pbkdf2_verify(password=plain_text, stored_hash=hashed_text)
                    if (verify):
                        print(Fore.GREEN + Style.BRIGHT + "\n[✓] Plain text match exacts with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break
                    else:
                        print(Fore.RED + Style.BRIGHT + "\n[X] Plain text does not match with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break

                #pbkdf2 with sha-512 header
                elif "$pbkdf2-sha512$100000$" in hashed_text:
                    print(Fore.YELLOW + Style.BRIGHT + "\nYour text was hashed in Pbkdf2 hash with SHA-512 hash algorithm")
                    plain_text = input(Style.BRIGHT + "Enter your plain text: ")

                    verify = pbkdf2_verify(password=plain_text, stored_hash=hashed_text)
                    if (verify):
                        print(Fore.GREEN + Style.BRIGHT + "\n[✓] Plain text match exacts with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break
                    else:
                        print(Fore.RED + Style.BRIGHT + "\n[X] Plain text does not match with the hashed text !")
                        prompt = input("\nContinue ? (yes/no): ").strip().lower()

                        if prompt == "yes":
                            utils.clear_output_area()
                            continue
                        elif prompt == "no":
                            utils.clear_output_area()
                            break
                        else: 
                            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
                            utils.clear_output_area()
                            break

                else:
                    print(Fore.YELLOW + Style.BRIGHT + "Warning: The text you provide is not a hashed text, or its hash algorithm is not supported by this program")
                    break


        elif choice == "3":
            print(Fore.RED + Style.BRIGHT + "Quitting...")
            sleep(1)
            utils.clear_output_area()
            utils.show_menu()
            break

        else:
            print(Fore.RED + Style.BRIGHT + "Invalid choice !")
            sleep(1)
            utils.clear_output_area()
            continue