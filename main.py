import os
import sys
import requests
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from threading import Thread
import subprocess
import time
import zipfile
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

# MADE BY voixys
# MAKE SURE THAT THE FILE YOU GOTTA DOWNLOAD IS A ZIP FILE OR ELSE IT'LL NOT WORK
# THE ICON FILE IS INSIDE ON A FOLDER NAMED "Interface"

file_url = "https://sample-videos.com/zip/10mb.zip" # LINK TO DOWNLOAD THE ZIP FILE
download_dir = os.path.expanduser(r"~\Application") # DOWNLOAD DIR
launch_file = os.path.expanduser(r"~\Application\big_buck_bunny_240p_10mb.mp4") # AFTER INSTALLITION LAUNCH FILE
print(launch_file)
print(download_dir)
application_name = "Application"
description = "The best application in the world"
theme = "dark" # AVAILABLE THEMES: light, dark

def unzip_file(zip_path, extract_to):
    try:
         with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
    except Exception as e:
        print(e)

class InstallerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(InstallerApp, self).__init__()
        if theme == "light":
            uic.loadUi(os.path.join("Interface\Light\Installer.ui"), self)
        else:
            uic.loadUi(os.path.join("Interface\Dark\Installer.ui"), self)

        self.install_application()
        self.setWindowTitle(f"{application_name} Installer")
        self.label.setText(f"Installing {application_name}...")
        self.label_2.setText(description)
        pixmap = QPixmap("Interface\icon.png")
        self.icon.setPixmap(pixmap)

    def install_application(self):
        self.download_thread = Thread(target=self.download_and_install, args=(file_url, download_dir))
        self.download_thread.start()

    def download_and_install(self, url, dest_folder):
        try:
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            filename = url.split("/")[-1]
            filepath = os.path.join(dest_folder, filename)

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            unzip_file(filepath, dest_folder)

            time.sleep(1)
            self.close()
            subprocess.Popen(launch_file)
        except Exception as e:
            print(e)
            time.sleep(1)
            self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InstallerApp()
    window.show()
    app.exec_()
