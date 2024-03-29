""" Utilities for adding a template emulator for a new IBEX device"""
import os

from templates.paths import EMULATOR_TEMPLATE
from utils.file_system_utils import copy_tree
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
        for dir in dirs:
            if default_name == dir:
                os.rename(path.join(root, dir), path.join(root, emulator_name))
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
    _copy_files(os.path.abspath(os.path.join(device_info.emulator_dir(), os.pardir)))
    _replace_default_name(os.path.abspath(os.path.join(device_info.emulator_dir(), os.pardir)), device_info.emulator_name())
