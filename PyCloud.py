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

        encryptIni(uncryptedIni,cryptedIni,password)

    
    return

# -------------------------------------------> changePassword
def validIni(iniFile):

    reader = configparser.ConfigParser()
    try:
        reader.read(iniFile)
        return True
    except configparser.ParsingError as error:
        print("The ini configuration file looks wrong : ")
        print(error)
        time.sleep(4)
        return False


def addSite(decrypt,crypt):


    try:

        # Display banner
        displayBanner()
        # Get password to decrypt ini gile
        password = input("[?] Please, enter the password to unlock ini file : ")
        # Decrypt the ini file to check if the synta is right
        decryptIni(crypt,decrypt,password)
        # If the ini file have incorrect syntax, go to menu
        if not validIni(decrypt):
            return main()
        # Else, add a new site to backup
        else:

            # Initiate config reader
            configReader = configparser.ConfigParser(delimiters=':')

            # Simple error condition with loop to get user answer
            # Choose folder to backup
            loop = True
            displayBanner()
            folderBackup = input("[?] Which folder do you want backup : ")
            while loop:
                displayBanner()
                if not os.path.isdir(folderBackup):
                    print(f"[!] The folder {folderBackup} does not exist")
                    folderBackup = input("[?] Which folder do you want backup : ")
                else:
                    configReader.add_section(folderBackup)
                    loop = False

            # Choose the targeted server where upload backup
            displayBanner()
            site = input("[?] Targeted server to save backup  (hostname or IP) : ")
            configReader.set(folderBackup,'site',site)

            # Choose the kind of backup
            # Mirror will make a simple mirror of local folder to a remote folder
            # Newest will upload only newest and news files
            loop = True
            displayBanner()
            mode = input("[?] What kind of backup do you want to do (mirror/newest) : ")
            while loop:
                displayBanner()
                if mode != 'mirror' and mode != 'newest':
                    print("[!] Please, make choice between (mirror/newest)")
                    mode = input("[?] What kind of backup do you want to do (mirror/newest) : ")
                else:
                    configReader.set(folderBackup,'mode',mode)
                    loop = False

            # Choose the backup protocol
            loop = True
            displayBanner()
            protocole = input("[?] Which protocole use (ssh/ftp) : ")
            while loop:
                displayBanner()
                if protocole != 'ssh' and protocole != 'ftp':
                    print(f"[!] The {protocole} protocole is not available...")
                    protocole = input("[?] Which protocole use (ssh/ftp) : ")
                else:
                    configReader.set(folderBackup,'protocole',protocole)
                    loop = False


            # Choose the port of the protocol
            loop = True
            displayBanner()
            port = input(f"[?] Which port do you want to use with {protocole} : ")
            while loop:
                displayBanner()
                if int(port) < 1 or int(port) > 65535:
                    print("[!] Please, choose a port between 1 and 65535")
                    port = input(f"[?] Which port do you want to use with {protocole} : ")
                else:
                    configReader.set(folderBackup,'port',port)
                    loop = False

            #---------------------------------------
            # If the user choose the FTP protocole |
            #---------------------------------------
            if protocole == 'ftp':

                # Want activation SSL/TLS with FTP ?
                loop = True
                displayBanner()
                ssl = input("[?] Do you want to use SSL/TLS (y/n) : ")
                while loop:
                    displayBanner()
                    if ssl != 'y' and ssl != 'n':
                        print("[!] Please, make choice between (y/n)")
                        ssl = input("[?] Do you want to use SSL/TLS (y/n) : ")
                    else:
                        configReader.set(folderBackup,'SSL/TLS',ssl)
                        loop = False

                # Which user to use with FTP ?
                loop = True
                displayBanner()
                user = input("[?] Which user use for FTP login : ")
                while loop:
                    displayBanner()
                    if len(user) == 0:
                        print("[!] Please, add a non empty username")
                        user = input("[?] Which user use for FTP login : ")
                    else:
                        configReader.set(folderBackup,'user',user)
                        loop = False

                # Which password ?
                displayBanner()
                passwd = input("[?] Which password use for FTP login : ")
                configReader.set(folderBackup,'password',passwd)
                        
            # ---------------------
            # If protocole is SSH |
            # ---------------------

            elif protocole == 'ssh':

                # Use a private key ?
                loop = True
                displayBanner()
                privateKey = input("[?] Do you want to use a private key with SSH (y/n) : ")
                while loop:
                    displayBanner()
                    if privateKey != 'y' and privateKey != 'n':
                        print("[!] Please make a choice between (y/n)")
                        privateKey = input("[?] Do you want to use a private key with SSH (y/n) : ")
                    else:
                        if str(privateKey) == 'y':
                            loop = True
                            displayBanner()
                            keyPath = input("[?] Specify the path of the private key : ")
                            while loop:
                                displayBanner()
                                if not os.path.isfile:
                                    print(f"[!] The key {keyPath} does not exist")
                                    keyPath = input("[?] Specify the path of the private key : ")
                                else:
                                    loop = False
                                    configReader.set(folderBackup,'key',keyPath)

                        elif str(privateKey) == 'n':

                            # If don't want to use a private key, which username to login ?
                            loop = True
                            displayBanner()
                            user = input("[?] Which user use for SSH login : ")
                            while loop:
                                displayBanner()
                                if len(user) == 0:
                                    print("[!] Please, add a non empty username")
                                    user = input("[?] Which user use for SSH login : ")
                                else:
                                    configReader.set(folderBackup,'user',user)
                                    loop = False

                            # Which password use to login
                            displayBanner()
                            passwd = input("[?] Which password use for SSH login : ")
                            configReader.set(folderBackup,'password',passwd)

            # Add a comment for this backup configuration ?
            loop = True
            displayBanner()
            comment = input("[?] Do you want to add a comment (y/n) : ")
            while loop:
                displayBanner()
                if comment != 'y' and comment != 'n':
                    print("[!] Please make a choice between (y/n)")
                    comment = input("[?] Do you want to add a comment (y/n) : ")
                else:
                    loop = False
            if str(comment) == 'y':
                readComment = input("[?] Add your comment to the backup configuration : \n")
                configReader.set(folderBackup,'comment',readComment)


            # Make a global view of the configuration
            loop = True
            while loop:
                displayBanner()
                print(f"[{folderBackup}]")
                for name,value in configReader.items(folderBackup):
                    print(f"{name} : {value}")

                response = input("\nConfirm backup configuration creation (y/n)")
                if response != 'y' and response != 'n':
                    displayBanner()
                    print(f"[{folderBackup}]")
                    for name,value in configReader.items(folderBackup):
                        print(f"{name} : {value}")
                    response = input("\nConfirm backup configuration creation (y/n)")
                else:
                    loop = False



            # Finally write the configuration in the ini file
            with open(decrypt,'a') as iniFile:
                configReader.write(iniFile)

            # Encrypt ini file at the end
            encryptIni(decrypt,crypt,password)

        return
    
    except KeyboardInterrupt:
        displayBanner()
        encryptIni(decrypt,crypt,password)
        print("\n[+] Successfully encrypted INI file before return to the menu")
        time.sleep(3)
        return main()





def main():


# -------------------------------------------------------
#                  Define some variables                 
# -------------------------------------------------------

    # Get home folder
    home = os.path.expanduser('~')
    # Define PyCloud folder
    pycloudFolder = f"{home}/.PyCloud"
    # Define INI file
    # Extension can be change for the encrypted ini file
    # The decrypt ini file must have INI extension (for configparser checking)
    encryptedIni = f"{pycloudFolder}/config.aes"
    decryptedIni = f"{pycloudFolder}/config.ini"

# --------------------------------------------------------
# ------------------ Begin of the script -----------------
# --------------------------------------------------------

    # It's better with a banner ! \o/
    displayBanner()

    # Check the installation at the begining
    checkConfig(encryptedIni,decryptedIni, pycloudFolder)

    # Diplay banner and initial decrypt INI file
    displayBanner()
    #password = input("[?] Use password to decrypt ini file : ")
    #decryptIni(encryptedIni,decryptedIni,password)

    # Large try
    try:

        displayBanner()
        print(
        """
        1. Launch backup
        2. Add a new folder for backup
        3. Change setting for a folder (modify a parameter)
        4. Remove a folder
        5. View backup settings
        6. Change encryption password

        99. Quit

        """
        )

        # Force type to choice
        choice = int(input("[?] Choose an action : "))

        if choice == 2:
            addSite(decryptedIni,encryptedIni)

        if choice == 5:
            displayBanner()
            password = input("[?] Please, enter the password to unlock ini file : ")
            


        elif choice == 99:
            exit()


    # If user quit the script with escape keys, encrypt ini file before quit
    except KeyboardInterrupt:
        encryptIni(decryptedIni,encryptedIni,password)
        print("\n[+] Successfully encrypted INI file before quit the script")


if __name__ == '__main__':
    main()





