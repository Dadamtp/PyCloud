#!/usr/bin/env python3


import configparser
import os
import time

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

# -------------------------------------------> checkConfig
def checkConfig(ini,folder):
# Function to check if initiale config is present

    # If PyCloud folder does not exist, create it and create the ini file too
    if not os.path.isdir(folder):
        print(f"[+] PyCloud folder does not exist yet")
        print(f"[+] Create {folder}")
        print(f"[+] Add ini file {ini}")
        os.mkdir(folder)
        file = open(ini,'w')
        file.close()
    # Else if PyCloud folder exist yet but ini file does not exist
    elif os.path.isdir(folder) and not os.path.isfile(iniFile):
        print(f"[+] Ini file does not exist yet")
        print(f"[+] Create {ini}")
        file = open(ini,'w')
        file.close()   

    # Make a sleep before refresh the banner 
    time.sleep(3)
    print('ok')

    return

# ========================================================
# ========================= Main =========================
# ========================================================

# Get home folder
home = os.path.expanduser('~')
# Define PyCloud folder
pycloudFolder = f"{home}/.PyCloud"
# Define INI file
iniFile = f"{home}/.PyCloud/config.ini"

# It's better with a banner ! \o/
displayBanner()

# Check the installation at the begining
checkConfig(iniFile, pycloudFolder)







