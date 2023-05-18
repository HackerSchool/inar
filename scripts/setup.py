from core import Parser
from zipfile import ZipFile

import os
import requests

import sys
import subprocess #https://docs.python.org/3/library/subprocess.html


# Files to download into the data directory.
FILES = [
    "https://raw.githubusercontent.com/kipr/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
    "https://raw.githubusercontent.com/kipr/opencv/master/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml",
    "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
]

PACKAGES = [
    "vosk", 
    "spacy", 
    "PyAudio"
]

def setup(dataDir):
    """Downloads the required files into the data directory."""

    # Create the data directory if it doesn't exist.
    if not os.path.exists(dataDir):
        os.mkdir(dataDir)

    for file in FILES:
        # Send a GET request to the file URL.
        print("Downloading file {}...".format(file))
        response = requests.get(file)
        if response.status_code != 200:
            print("Failed to download file {}, error {}".format(file, response.status_code))
            continue

        # Write the file to the data directory.
        filename = os.path.basename(file)
        path = os.path.join(dataDir, filename)
        open(path, "wb").write(response.content)
    
    # Loading the temp.zip and creating a zip object
    with ZipFile("../data/vosk-model-small-en-us-0.15.zip", 'r') as zObject:
    
        # Extracting the zip
        zObject.extractall(path="../data")
    
    # Delete the zip file
    os.remove("../data/vosk-model-small-en-us-0.15.zip")

    
def install_packages():
    """Install the required python libraries."""

    for package in PACKAGES:
        print("Downloading python library {}...".format(package))
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL)
        except Exception as e:
            print("Failed to download library {}".format(package))
            print("Exception {}".format(e))


if __name__ == "__main__":
    # Default data directory is `../data` relative to this file.
    defaultDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")

    parser = Parser()
    parser.add("help", "Prints this help message.", default=False)
    parser.add("data", "Path to the data directory.", default=defaultDataDir)
    options = parser.parse()

    if options["help"]:
        print(parser.help())
    else:
        setup(options["data"])
        install_packages()
