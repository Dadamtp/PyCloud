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


    return

# -------------------------------------------> decryptIni
def decryptIni(aes,password):
# Function to decrypt ini file

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


    return 




# -------------------------------------------> checkConfig
def checkConfig(cryptIni,folder):
# Function to check if initiale config is present

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
        encryptIni(noncryptedIni,password)
        
    # Else if PyCloud folder exist yet but ini encrypted file does not exist
    elif os.path.isdir(folder) and not os.path.isfile(cryptIni):
        print(f"[+] Ini file does not exist yet")
        print(f"[+] Create {noncryptedIni}")
        file = open(noncryptedIni,'w')
        file.close()
        password = input("[?] Choose a password for the ini file encryption : ")
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
#displayBanner()

# Check the installation at the begining
checkConfig(iniFile, pycloudFolder)







