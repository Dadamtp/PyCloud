#!/usr/bin/env python3

import os
import glob
import time
import pathlib
import pyAesCrypt
import configparser


def displayBanner():

    os.system('clear')
    print("""
  _____        _____ _                 _ 
 |  __ \      / ____| |               | |
 | |__) |   _| |    | | ___  _   _  __| |
 |  ___/ | | | |    | |/ _ \| | | |/ _` |
 | |   | |_| | |____| | (_) | |_| | (_| |
 |_|    \__, |\_____|_|\___/ \__,_|\__,_|
         __/ |                           
        |___/                            
    """)

    return


# -------------------------------------------> encryptIni
def encryptIni(inputFile,ouputFile,password):
# Function to encrypt the ini configuration file
    
    try:

        # Buffer initialization
        bufferSize = 64 * 1024
        # Crypt the file
        pyAesCrypt.encryptFile(inputFile,ouputFile,password,bufferSize)
        # Remove the original file
        os.remove(inputFile)

    except Exception as error:
        print(f"[!] {error}")
        exit()

    return

# -------------------------------------------> decryptIni
def decryptIni(inputFile,outputFile,password):
# Function to decrypt ini file

    try:

        # Buffer initialization
        bufferSize = 64 * 1024
        # Decrypt ini file
        pyAesCrypt.decryptFile(inputFile,outputFile,password,bufferSize)
        # Remove the original file
        os.remove(inputFile)

    # If the password is incorrect...or other exception
    except Exception as error:
        print(f"[!] {error}")
        exit()


    return 


# -------------------------------------------> checkConfig
def checkConfig(cryptedIni,uncryptedIni,folder):
# Function to check if initiale config is present

    # Define the ini file when is decrypted
    #noncryptedIni = f"{folder}/config.ini"
    
    # If PyCloud folder does not exist, create it and create the ini encrypted file too
    if not os.path.isdir(folder):
        print(f"[+] PyCloud folder does not exist yet")
        print(f"[+] Create {folder}")
        print(f"[+] Add ini file {cryptedIni}")
        os.mkdir(folder)
        file = open(uncryptedIni,'w')
        file.close()
        password = input("[?] Choose a password for the ini file encryption : ")
        # Add error condition if the input password is empty
        if len(password) == 0:
            notValid = True
        else:
            notValid = False
        # While the password is empty, make a while loop
        while notValid:
            displayBanner()
            print("[!] The encryption password cannot be empty")
            password = input("[?] Choose a password for the ini file encryption : ")
            if len(password) > 0:
                notValid = False
                            
        encryptIni(uncryptedIni,cryptedIni,password)
        
    # Else if PyCloud folder exist yet but ini encrypted file does not exist
    elif os.path.isdir(folder) and not os.path.isfile(cryptedIni):
        print(f"[+] Ini file does not exist yet")
        print(f"[+] Create {uncryptedIni}")
        file = open(uncryptedIni,'w')
        file.close()
        password = input("[?] Choose a password for the ini file encryption : ")
        # Add error condition if the input password is empty
        if len(password) == 0:
            notValid = True
        else:
            notValid = False
        # While the password is empty, make a while loop
        while notValid:
            displayBanner()
            print("[!] The encryption password cannot be empty")
            password = input("[?] Choose a password for the ini file encryption : ")
            if len(password) > 0:
                notValid = False

        encryptIni(uncryptedIni,encryptedIni,password)

    
    return

# ========================================================
# ========================= Main =========================
# ========================================================

# Get home folder
home = os.path.expanduser('~')
# Define PyCloud folder
pycloudFolder = f"{home}/.PyCloud"
# Define INI file
encryptedIni = f"{pycloudFolder}/config.aes"
decryptedIni = f"{pycloudFolder}/config.ini"

# It's better with a banner ! \o/
displayBanner()

# Check the installation at the begining
checkConfig(encryptedIni,decryptedIni, pycloudFolder)

# Diplay banner and initial decrypt INI file
displayBanner()
password = input("[?] Use password to decrypt ini file : ")
decryptIni(encryptedIni,decryptedIni,password)


displayBanner()
print(
"""
1. Add remote site to configure backup
2. Change remote site (modify a parameter)
3. Remove remote 
4. Check INI file (check if the syntax work properly)

99. Quit
"""
)

choice = int(input("[?] Choose an action : "))

if choice == 99:
    encryptIni(decryptedIni,encryptedIni,password)
    print("[+] Successfully encrypted INI file")
    exit()








