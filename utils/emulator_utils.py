""" Utilities for adding a template emulator for a new IBEX device"""
from templates.paths import EMULATOR_TEMPLATE
from file_system_utils import copy_tree
from os import path, walk
import logging
from device_info_generator import DeviceInfoGenerator


def _copy_files(emulator_dir):
    """
    :param emulator_dir: Directory of the device emulator
    """
    logging.info("Copying template emulator to {}".format(emulator_dir))
    copy_tree(EMULATOR_TEMPLATE, emulator_dir)


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
