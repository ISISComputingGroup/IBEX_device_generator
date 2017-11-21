""" Utilities for adding a template emulator for a new IBEX device"""
from templates.paths import EMULATOR_TEMPLATE
from system_paths import LEWIS_EMULATORS
from shutil import copytree
from os import path, walk
import logging
from device_info_generator import DeviceInfoGenerator


def _copy_files(info_generator):
    """
    :param device: Name of the device
    """
    dst = info_generator.emulator_dir()
    logging.info("Copying template emulator to {}".format(dst))
    if path.exists(dst):
        raise RuntimeError("Unable to create template emulator in {}, directory already exists".format(dst))
    copytree(EMULATOR_TEMPLATE, dst)


def _replace_default_name(info_generator):
    """
    :param device: Name of the device
    """
    default_name = "DEVICENAME"
    for root, dirs, files in walk(info_generator.emulator_dir()):
        for filename in files:
            with open(path.join(root, filename)) as f:
                lines = [l.replace(default_name, info_generator.emulator_name()) for l in f.readlines()]
            with open(path.join(root, filename), "w") as f:
                f.writelines(lines)


def create_emulator(device):
    """
    Creates a vanilla emulator in the DeviceEmulator submodule
    :param device: Name of the device to create the emulator for
    """
    info_generator = DeviceInfoGenerator(device)
    _copy_files(info_generator)
    _replace_default_name(info_generator)
