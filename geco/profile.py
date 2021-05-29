import logging
import os
import shutil
import yaml


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
