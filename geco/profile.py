import augeas
import glob
import hashlib
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import yaml
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Profile:
    def __init__(self, path):
        self.path = str(path)
        self.efi_dir = str(path) + "/EFI"

    def load(self):
        try:
            with open(self.path + "/geco.yaml", "r") as stream:
                try:
                    self.config = yaml.safe_load(stream)
                except yaml.YAMLError as e:
                    logging.fatal(e)
        except IOError:
            logging.fatal("Can't open " + self.path + "/geco.yaml")
            raise
        logging.debug("Profile loaded")

    def create_efi_dir(self):
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

    def checksum(self):
        logging.debug("Checking md5sum")
        with open(self.path + "/md5sum.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                md5sum, filename = line.split()
                filename = self.path + "/" + filename
                logging.debug("Checking file: " + filename)
                m = md5(filename)
                logging.debug("md5 = " + m)
                logging.debug("exprected md5 = " + md5sum)
                if m != md5sum:
                    raise Exception

    def download_opencore(self):
        try:
            zipurl_prefix = "https://github.com/dortania/build-repo/releases/download/OpenCorePkg-" + self.config["opencore"]["prerelease"]
        except KeyError:
            zipurl_prefix = "https://github.com/acidanthera/OpenCorePkg/releases/download/" + self.config["opencore"]["version"]
        zipurl = zipurl_prefix + "/OpenCore-" + self.config["opencore"]["version"] + "-" + self.config["opencore"]["variant"] + ".zip"
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
                    zfile.extract("X64/EFI/OC/Tools/OpenShell.efi", path=tmpdirname)
                    shutil.move(tmpdirname + "/X64/EFI/OC/Tools/OpenShell.efi", self.efi_dir + "/OC/Tools/OpenShell.efi")
                    zfile.extract("Docs/Sample.plist", path=tmpdirname)
                    shutil.move(tmpdirname + "/Docs/Sample.plist", self.efi_dir + "/OC/Config.plist")

    def download_kexts(self):
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

    def download_ocbinarydata(self):
        ref = self.config["opencore"]["OcBinaryData-ref"]
        zipurl = "https://github.com/acidanthera/OcBinaryData/archive/" + ref + ".zip"
        logging.info("Downloading " + zipurl + "...")
        with tempfile.TemporaryDirectory() as tmpdirname:
            with urlopen(zipurl) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(path=tmpdirname)
                    shutil.move(tmpdirname + "/OcBinaryData-" + ref + "/Drivers/HfsPlus.efi", self.efi_dir + "/OC/Drivers/HfsPlus.efi")
                    shutil.move(tmpdirname + "/OcBinaryData-" + ref + "/Resources", self.efi_dir + "/OC")

    def compile_ssdts(self):
        cwd = os.getcwd()
        os.chdir(self.path + "/SSDTs")
        for ssdt in glob.glob("SSDT-*.dsl"):
            aml_file = self.efi_dir + "/OC/ACPI/" + os.path.splitext(ssdt)[0] + ".aml"
            logging.debug("Compiling " + ssdt + " to " + aml_file)
            subprocess.run(["iasl", "-p", aml_file, ssdt])
        os.chdir(cwd)

    def patch_config_plist(self):
        MYROOT = self.efi_dir + "/OC"
        a = augeas.Augeas(root=MYROOT, flags=augeas.Augeas.NO_LOAD+augeas.Augeas.NO_MODL_AUTOLOAD)
        a.add_transform("Xml", "/Config.plist")
        a.load()
        a.set("/augeas/context", "/files/Config.plist/plist/dict")
        logging.debug("/augeas/root=" + a.get("/augeas/root"))
        logging.debug("/augeas/context=" + a.get("/augeas/context"))
        logging.debug("/augeas/load/Xml/lens=" + a.get("/augeas/load/Xml/lens"))
        logging.debug("/augeas/load/Xml/incl=" + a.get("/augeas/load/Xml/incl"))

        logging.debug("Remove warnings")
        a.remove("string[preceding-sibling::key[#text =~ regexp('^#WARNING - .*')]]")
        a.remove("key[#text =~ regexp('^#WARNING - .*')]")

        logging.debug("Adding ACPI files to Config.plist")
        directory = self.efi_dir + "/OC/ACPI"
        a.defvar("ACPI", "dict[preceding-sibling::key[#text='ACPI']][1]")
        a.defvar("ACPI_Add", "$ACPI/array[preceding-sibling::key[#text='Add']][1]")
        a.remove("$ACPI_Add/dict")

        for entry in glob.iglob(directory + '/*.aml'):
            logging.debug("Found aml file: " + os.path.basename(entry))
            a.defnode("mynode", "$ACPI_Add/dict[last()+1]", "")
            a.set("$mynode/key[last()+1]/#text", "Comment")
            a.set("$mynode/string[last()+1]/#text", os.path.basename(entry))
            a.set("$mynode/key[last()+1]/#text", "Enabled")
            a.set("$mynode/true[last()+1]", "#empty")
            a.set("$mynode/key[last()+1]/#text", "Path")
            a.set("$mynode/string[last()+1]/#text", os.path.basename(entry))

        logging.debug("Remove default ACPI patches from Config.plist")
        a.defvar("ACPI_Patch", "$ACPI/array[preceding-sibling::key[#text='Patch']][1]")
        a.remove("$ACPI_Patch/dict")

        logging.debug("Adding Kexts to Config.plist")
        directory = self.efi_dir + "/OC/Kexts"
        a.defvar("Kernel", "dict[preceding-sibling::key[#text='Kernel']][1]")
        a.defvar("Kernel_Add", "$Kernel/array[preceding-sibling::key[#text='Add']][1]")
        a.remove("$Kernel_Add/dict")
        for entry in glob.iglob(directory + '/**/*.kext', recursive=True):
            logging.debug("Found Kext: " + os.path.basename(entry))
            a.defnode("mynode", "$Kernel_Add/dict[last()+1]", "")
            a.set("$mynode/key[last()+1]/#text", "Arch")
            a.set("$mynode/string[last()+1]/#text", "x86_64")
            a.set("$mynode/key[last()+1]/#text", "BundlePath")
            a.set("$mynode/string[last()+1]/#text", os.path.relpath(entry, directory))
            a.set("$mynode/key[last()+1]/#text", "Comment")
            a.set("$mynode/string[last()+1]", None)
            a.set("$mynode/key[last()+1]/#text", "Enabled")
            a.set("$mynode/true[last()+1]", "#empty")
            a.set("$mynode/key[last()+1]/#text", "ExecutablePath")
            a.set("$mynode/string[last()+1]/#text", "Contents/MacOS/" + os.path.splitext(os.path.basename(entry))[0])
            a.set("$mynode/key[last()+1]/#text", "MaxKernel")
            a.set("$mynode/string[last()+1]", None)
            a.set("$mynode/key[last()+1]/#text", "MinKernel")
            a.set("$mynode/string[last()+1]", None)
            a.set("$mynode/key[last()+1]/#text", "PlistPath")
            a.set("$mynode/string[last()+1]/#text", "Contents/Info.plist")

        logging.debug("Adding Tools to Config.plist")
        directory = self.efi_dir + "/OC/Tools"
        a.defvar("Misc", "dict[preceding-sibling::key[#text='Misc']][1]")
        a.defvar("Tools", "$Misc/array[preceding-sibling::key[#text='Tools']][1]")
        a.remove("$Tools/dict")
        for entry in glob.iglob(directory + '/*.efi'):
            logging.debug("Found Tool: " + os.path.basename(entry))
            a.defnode("mynode", "$Tools/dict[last()+1]", "")
            a.set("$mynode/key[last()+1]/#text", "Arguments")
            a.set("$mynode/string[last()+1]", None)
            a.set("$mynode/key[last()+1]/#text", "Auxiliary")
            a.set("$mynode/true[last()+1]", "#empty")
            a.set("$mynode/key[last()+1]/#text", "Comment")
            a.set("$mynode/string[last()+1]/#text", os.path.basename(entry))
            a.set("$mynode/key[last()+1]/#text", "Enabled")
            a.set("$mynode/true[last()+1]", "#empty")
            a.set("$mynode/key[last()+1]/#text", "Flavour")
            a.set("$mynode/string[last()+1]/#text", "Auto")
            a.set("$mynode/key[last()+1]/#text", "Name")
            a.set("$mynode/string[last()+1]/#text", os.path.basename(entry))
            a.set("$mynode/key[last()+1]/#text", "Path")
            a.set("$mynode/string[last()+1]/#text", os.path.basename(entry))
            a.set("$mynode/key[last()+1]/#text", "RealPath")
            a.set("$mynode/false[last()+1]", "#empty")
            a.set("$mynode/key[last()+1]/#text", "TextMode")
            a.set("$mynode/false[last()+1]", "#empty")

        logging.debug("Adding Drivers to Config.plist")
        directory = self.efi_dir + "/OC/Drivers"
        a.defvar("UEFI", "dict[preceding-sibling::key[#text='UEFI']][1]")
        a.defvar("Drivers", "$UEFI/array[preceding-sibling::key[#text='Drivers']][1]")
        a.remove("$Drivers/string")
        for entry in glob.iglob(directory + '/*.efi'):
            logging.debug("Found Drivers: " + os.path.basename(entry))
            a.set("$Drivers/string[last()+1]/#text", os.path.basename(entry))

        with open(self.path + "/config.augtool", "r") as file:
            transformations = file.read()
            logging.debug("Applying Augeas transformations: " + transformations)
            a.srun(sys.stdout, transformations)

        try:
            a.save()
        except augeas.AugeasIOError:
            for p in a.match("/augeas//error"):
                logging.error(a.get(p) + ": " + a.get(p + "/message"))
            sys.exit(1)

        logging.debug("Prettify Config.plist")
        tree = ET.parse(self.efi_dir + "/OC/Config.plist")
        ET.indent(tree.getroot()[0], space="\t", level=0)

        logging.debug("Canonicalize Config.plist")
        with open(self.efi_dir + "/OC/Config.plist", mode='w', encoding='utf-8') as out_file:
            ET.canonicalize(ET.tostring(tree.getroot()), out=out_file)
