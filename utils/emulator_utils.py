""" Utilities for adding a template emulator for a new IBEX device"""
from templates.paths import TEMPLATE_EMULATOR
from system_paths import LEWIS_EMULATORS
from shutil import copytree
from os import path, walk
import logging


def _copy_files(device):
    """
    :param device: Name of the device
    """
    dst = path.join(LEWIS_EMULATORS, device)
    logging.info("Copying template emulator to {}".format(dst))
    if path.exists(dst):
        raise RuntimeError("Unable to create template emulator in {}, directory already exists".format(dst))
    copytree(TEMPLATE_EMULATOR, dst)


def _replace_default_name(device):
    """
    :param device: Name of the device
    """
    default_name = "DEVICENAME"
    emulators_src = path.join(LEWIS_EMULATORS, device)
    for root, dirs, files in walk(emulators_src):
        for filename in files:
            with open(path.join(root, filename)) as f:
                lines = [l.replace(default_name, device) for l in f.readlines()]
            with open(path.join(root, filename), "w") as f:
                f.writelines(lines)


def create_emulator(device):
    """
    Creates a vanilla emulator in the DeviceEmulator submodule
    :param device: Name of the device to create the emulator for
    """
    _copy_files(device)
    _replace_default_name(device)