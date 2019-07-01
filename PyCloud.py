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
def encryptIni(ini,password):
# Function to encrypt the ini configuration file
    
    try:

        # Buffer initialization
        bufferSize = 64 * 1024
        # Get the basename of ini file
        baseName = (os.path.basename(ini)).split('.')[0]
        # Get the parent folder of the ini file
        parentFolder = pathlib.Path(ini).parent
        # Define a extension for the encrypted ini file
        extension = 'aes'
        # Create the fullname for the encrypted file
        fullnameCryptedFile = f"{parentFolder}/{baseName}.{extension}"
        # Crypt the file
        pyAesCrypt.encryptFile(ini,fullnameCryptedFile,password,bufferSize)
        # Remove the original file
        os.remove(ini)

    except Exception as error:
        print(f"[!] {error}")
        exit()

    return

# -------------------------------------------> decryptIni
def decryptIni(aes,password):
# Function to decrypt ini file

    try:

        # Buffer initialization
        bufferSize = 64 * 1024
        # Get the basename of the encrypted ini file
        baseName = (os.path.basename(aes)).split('.')[0]
        # Get the parent folder of the encrypted ini file
        parentFolder = pathlib.Path(aes).parent
        # Define extension for output decrypted file
        extension = 'ini'
        # Define the fullname of the decrypted file
        fullnameDecryptedFile = f"{parentFolder}/{baseName}.{extension}"
        # Decrypt ini file
        pyAesCrypt.decryptFile(aes,fullnameDecryptedFile,password,bufferSize)
        # Remove the original file
        os.remove(aes)

    # If the password is incorrect...or other exception
    except Exception as error:
        print(f"[!] {error}")
        exit()


    return 




# -------------------------------------------> checkConfig
def checkConfig(cryptIni,folder):
# Function to check if initiale config is present

    # Define the ini file when is decrypted
    noncryptedIni = f"{folder}/config.ini"
    
    # If PyCloud folder does not exist, create it and create the ini encrypted file too
    if not os.path.isdir(folder):
        print(f"[+] PyCloud folder does not exist yet")
        print(f"[+] Create {folder}")
        print(f"[+] Add ini file {cryptIni}")
        os.mkdir(folder)
        file = open(noncryptedIni,'w')
        file.close()
        password = input("[?] Choose a password for the ini file encryption : ")
        # Add error condition if the input password is empty
        if len(password) == 0:
            notValid = True
        # While the password is empty, make a while loop
        while notValid:
            displayBanner()
            print("[!] The encryption password cannot be empty")
            password = input("[?] Choose a password for the ini file encryption : ")
            if len(password) > 0:
                notValid = False
                            
        encryptIni(noncryptedIni,password)
        
    # Else if PyCloud folder exist yet but ini encrypted file does not exist
    elif os.path.isdir(folder) and not os.path.isfile(cryptIni):
        print(f"[+] Ini file does not exist yet")
        print(f"[+] Create {noncryptedIni}")
        file = open(noncryptedIni,'w')
        file.close()
        password = input("[?] Choose a password for the ini file encryption : ")
        # Add error condition if the input password is empty
        if len(password) == 0:
            notValid = True
        # While the password is empty, make a while loop
        while notValid:
            displayBanner()
            print("[!] The encryption password cannot be empty")
            password = input("[?] Choose a password for the ini file encryption : ")
            if len(password) > 0:
                notValid = False

        encryptIni(noncryptedIni,password)

    
    return

# ========================================================
# ========================= Main =========================
# ========================================================

# Get home folder
home = os.path.expanduser('~')
# Define PyCloud folder
pycloudFolder = f"{home}/.PyCloud"
# Define INI file
iniFile = f"{home}/.PyCloud/config.aes"

# It's better with a banner ! \o/
displayBanner()

# Check the installation at the begining
checkConfig(iniFile, pycloudFolder)

# Diplay banner and initial decrypt INI file
displayBanner()
password = input("[?] Use password to decrypt ini file : ")
decryptIni(iniFile,password)


displayBanner()
print(
"""
1. Add remote site to configure backup
2. Change remote site (modify a parameter)
3. Remove remote 
4. Check INI file (check if the syntax work properly)
"""
)

input("[?] Choose an action : ")









