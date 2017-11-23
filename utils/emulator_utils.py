""" Utilities for adding a template emulator for a new IBEX device"""
from templates.paths import EMULATOR_TEMPLATE
from file_system_utils import copy_tree
from os import path, walk
import logging


def _copy_files(emulator_dir):
    """
    Args:
        emulator_dir: Directory of the device emulator
    """
    logging.info("Copying template emulator to {}".format(emulator_dir))
    copy_tree(EMULATOR_TEMPLATE, emulator_dir)


def _replace_default_name(emulator_dir, emulator_name):
    """
    Args:
        emulator_dir: Directory where the emulator lives
        emulator_name: Name given to the emulator
    """
    default_name = "DEVICENAME"
    for root, dirs, files in walk(emulator_dir):
        for filename in files:
            with open(path.join(root, filename)) as f:
                lines = [l.replace(default_name, emulator_name) for l in f.readlines()]
            with open(path.join(root, filename), "w") as f:
                f.writelines(lines)


def create_emulator(device_info):
    """
    Creates a vanilla emulator in the DeviceEmulator submodule

    Args:
        device_info: Provides name-based information about the device
    """
    _copy_files(device_info.emulator_dir())
    _replace_default_name(device_info.emulator_dir(), device_info.emulator_name())
