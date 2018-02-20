import urllib.request, urllib.parse, json, os.path, re, string, time

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def file_put_contents(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()
    return True

def format_filename(s): # Thank: https://gist.github.com/seanh/93666
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

class backupUtility:

    def getCurrentFiles(self):

        if os.path.isfile(self.indexFile):
            self.currentFiles = json.loads(file_get_contents(self.indexFile))
        else:
            file_put_contents(self.indexFile, "{}")
            self.currentFiles = {}

    def __init__(self):

        self.indexFile = "index.json"
        self.storageDir = "files"

        if not os.path.isdir(self.storageDir):
            os.mkdir(self.storageDir)

        data = {
            'auth_token' : file_get_contents('./apitoken.txt')
        }

        data = bytes( urllib.parse.urlencode( data ).encode() )
        handler = urllib.request.urlopen( 'https://www.museum-digital.de/sandkasten3/musdb/lists.php?musid=1', data );
        self.files = ( handler.read().decode( 'utf-8' ) )

        self.getCurrentFiles()

        for file in json.loads(self.files):
            if file["location"] in self.currentFiles and file["update_date"] == self.currentFiles[file["location"]]:
                pass
            else:
                try:
                    urllib.request.urlretrieve (file["location"], self.storageDir + "/" + format_filename(file["location"]))

                    print("Downloaded: " + file["location"])
                    self.currentFiles[file["location"]] = file["update_date"]
                    time.sleep(3)
                except:
                    print("Could not download " + file["location"])

        # os.rmfile(self.indexFile)
        file_put_contents(self.indexFile, json.dumps(self.currentFiles))

if __name__ == "__main__":

    backupRun = backupUtility()

    input("Press any key to exit")
