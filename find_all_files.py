from pathlib import Path
from os.path import abspath
import shutil
import os


def findFilesAndCopyToExtensionFolder(extension, path):
    """Find the files and copy to the extension folder

    Args:
        extension (string): "Name of the Extension"
        Path (string): Path Where Files to Stored.
    """
    FOLDER = fr"{path}/{extension}"

    if not (os.path.exists(FOLDER)):
        os.mkdir(FOLDER)
    root = Path.home()  # take the Home directory as root

    list_of_files = []
    for path in Path(root).glob(f"**/*.{extension}"):
        filename = abspath(path)
        print(filename)
        list_of_files.append(filename)

        head, tail = os.path.split(filename)
        if tail in os.listdir(FOLDER):
            continue
        shutil.copy(src=filename, dst=FOLDER)

    print(len(list_of_files))

findFilesAndCopyToExtensionFolder("zip", r"C:\Users\achyu\OneDrive\Documents")