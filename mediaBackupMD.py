#!/usr/bin/env python3

import urllib.request, urllib.parse, json, os.path, re, string, time
import xml.etree.ElementTree as ET

# General shortcut functions

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def file_put_contents(filename, content):
    with open(filename, "w") as f:
        f.write(content)
        f.close()
        return True

# Function to escape filenames.
# Necessary to save all files in one folder.

def format_filename(s): # Thank: https://gist.github.com/seanh/93666
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

class backupUtility:

    # Load index of already downloaded files and the last times they were updated
    # to prevent the need for double-downloading the files

    def getCurrentFiles(self):

        if os.path.isfile(self.indexFile):
            self.currentFiles = json.loads(file_get_contents(self.indexFile))
        else:
            file_put_contents(self.indexFile, "{}")
            self.currentFiles = {}

    def getSettings(self): # Function reading the settings. Exits the script in case of any problems

        try:

            tree = ET.parse('settings.xml')
            root = tree.getroot()

            self.auth_token = root.findall("authtoken")[0].text
            self.url = root.findall("url")[0].text

        except:

            print("Error: Settings.xml could not be read.")
            exit()

    def __init__(self):

        self.getSettings()

        self.indexFile = "index.json"
        self.storageDir = "files"

        if not os.path.isdir(self.storageDir): # Ensure that the storage directory exists.
            os.mkdir(self.storageDir)

        # Read current index from URL

        data = {
            'auth_token' : self.auth_token
        }

        data = bytes( urllib.parse.urlencode( data ).encode() )
        handler = urllib.request.urlopen( self.url, data );
        self.files = (handler.read().decode('utf-8'))

        self.getCurrentFiles() # Read index of already downloaded files

        for file in json.loads(self.files): # Loop over current

            # If the file already exists and the update dates equal, do nothing
            if file["location"] in self.currentFiles and file["update_date"] == self.currentFiles[file["location"]]:
                pass
            else:

                # Try downloading the image / resource and log it
                try:
                    newFileName = self.storageDir + "/" + format_filename(file["location"])

                    if os.path.isfile(newFileName):
                        os.remove(newFileName)

                    urllib.request.urlretrieve (file["location"], newFileName)

                    # Provide feedback and log the download
                    print("Downloaded: " + file["location"])
                    self.currentFiles[file["location"]] = file["update_date"]

                    time.sleep(3) # Sleep a bit to reduce resource-intensity

                except:
                    print("Could not download " + file["location"])

        # Save log
        file_put_contents(self.indexFile, json.dumps(self.currentFiles))

if __name__ == "__main__":

    backupRun = backupUtility()

    input("Press any key to exit")
