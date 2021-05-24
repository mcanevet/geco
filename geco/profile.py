import logging
import os
import glob
from posixpath import basename
import yaml
import tempfile
import shutil
from pathlib import Path
import subprocess
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

class Profile:
    def __init__(self, path):
        self.path = path
        self.efi_dir = path + "/EFI"
        self._load()
        self._create_efi_dir()
        self._compile_ssdts()
        self._download_kexts()
        self._download_opencore()
        self._download_ocbinarydata()

    def _create_efi_dir(self):
        try:
            shutil.rmtree(self.efi_dir)
        except FileNotFoundError:
            pass
        if not os.path.exists(self.efi_dir):
            os.makedirs(self.efi_dir)
        if not os.path.exists(self.efi_dir + "/BOOT"):
            os.makedirs(self.efi_dir + "/BOOT")
        if not os.path.exists(self.efi_dir + "/OC"):
            os.makedirs(self.efi_dir + "/OC")
        if not os.path.exists(self.efi_dir + "/OC/Tools"):
            os.makedirs(self.efi_dir + "/OC/Tools")
        if not os.path.exists(self.efi_dir + "/OC/Kexts"):
            os.makedirs(self.efi_dir + "/OC/Kexts")
        if not os.path.exists(self.efi_dir + "/OC/Drivers"):
            os.makedirs(self.efi_dir + "/OC/Drivers")
        if not os.path.exists(self.efi_dir + "/OC/ACPI"):
            os.makedirs(self.efi_dir + "/OC/ACPI")

    def _load(self):
        try:
            with open(self.path + "/geco.yaml", "r") as stream:
                try:
                    self.config = yaml.safe_load(stream)
                    logging.debug(self.config["opencore"]["version"])
                except yaml.YAMLError as exc:
                    logging.fatal(exc)
        except IOError:
            logging.fatal("Can't open " + self.path + "/geco.yaml")

    def _download_opencore(self):
        zipurl = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + self.config["opencore"]["version"] + "/OpenCore-" + self.config["opencore"]["version"] + "-" + self.config["opencore"]["variant"] + ".zip"
        logging.info("Downloading " + zipurl + "...")
        with tempfile.TemporaryDirectory() as tmpdirname:
            with urlopen(zipurl) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extract("X64/EFI/BOOT/BOOTx64.efi", path=tmpdirname)
                    shutil.move(tmpdirname + "/X64/EFI/BOOT/BOOTx64.efi", self.efi_dir + "/BOOT/BOOTx64.efi")
                    zfile.extract("X64/EFI/OC/OpenCore.efi", path=tmpdirname)
                    shutil.move(tmpdirname + "/X64/EFI/OC/OpenCore.efi", self.efi_dir + "/OC/OpenCore.efi")
                    zfile.extract("X64/EFI/OC/Drivers/OpenRuntime.efi", path=tmpdirname)
                    shutil.move(tmpdirname + "/X64/EFI/OC/Drivers/OpenRuntime.efi", self.efi_dir + "/OC/Drivers/OpenRuntime.efi")
                    zfile.extract("X64/EFI/OC/Drivers/OpenCanopy.efi", path=tmpdirname)
                    shutil.move(tmpdirname + "/X64/EFI/OC/Drivers/OpenCanopy.efi", self.efi_dir + "/OC/Drivers/OpenCanopy.efi")
                    zfile.extract("Docs/Sample.plist", path=tmpdirname)
                    shutil.move(tmpdirname + "/Docs/Sample.plist", self.efi_dir + "/OC/Config.plist")

    def _download_ocbinarydata(self):
        ref = self.config["opencore"]["OcBinaryData-ref"]
        zipurl = "https://github.com/acidanthera/OcBinaryData/archive/" + ref + ".zip"
        logging.info("Downloading " + zipurl + "...")
        with tempfile.TemporaryDirectory() as tmpdirname:
            with urlopen(zipurl) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(path=tmpdirname)
                    shutil.move(tmpdirname + "/OcBinaryData-" + ref + "/Drivers/HfsPlus.efi", self.efi_dir + "/OC/Drivers/HfsPlus.efi")
                    shutil.move(tmpdirname + "/OcBinaryData-" + ref + "/Resources", self.efi_dir + "/OC")

    def _download_kexts(self):
        for kext in self.config["kexts"]:
            zipurl = kext["source"]
            files = kext["files"]
            logging.info("Downloading " + zipurl + "...")
            with tempfile.TemporaryDirectory() as tmpdirname:
                with urlopen(zipurl) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        for file in zfile.namelist():
                            if file.startswith(tuple([sub + "/" for sub in files])):
                                logging.debug("Extracting " + file)
                                zfile.extract(file, path=tmpdirname)
                for file in files:
                    logging.debug("Moving " + tmpdirname + "/" + file + " into " + self.efi_dir + "/OC/Kexts")
                    shutil.move(tmpdirname + "/" + file, self.efi_dir + "/OC/Kexts/")

    def _compile_ssdts(self):
        cwd = os.getcwd()
        os.chdir(self.path + "/SSDTs")
        for ssdt in glob.glob("*.dsl"):
            aml_file = cwd + "/" + self.efi_dir + "/OC/ACPI/" + os.path.splitext(ssdt)[0] + ".aml"
            logging.debug("Compiling " + ssdt + " to " + aml_file)
            subprocess.run(["iasl", "-p", aml_file, ssdt])
        os.chdir(cwd)
