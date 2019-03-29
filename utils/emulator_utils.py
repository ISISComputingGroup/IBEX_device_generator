""" Utilities for adding a template emulator for a new IBEX device"""
from templates.paths import EMULATOR_TEMPLATE
from file_system_utils import copy_tree
from os import path, walk
import logging


def _add_emulator_directory_tree(device_info):
    """
    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        directory (Str): The directory files have been copied to
    """
    directory = device_info.emulator_dir()
    logging.info("Copying template emulator to {}".format(directory))
    copy_tree(EMULATOR_TEMPLATE, directory)

    return directory


def _replace_default_device_name(device_info):
    """
    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        files_changed (list[Str]): List of unique files that have been changed/created
    """
    emulator_name = device_info.emulator_name()
    emulator_dir = device_info.emulator_dir()

    for root, dirs, files in walk(emulator_dir):
        for filename in files:
            with open(path.join(root, filename)) as f:
                lines = [l.replace("DEVICENAME", emulator_name) for l in f.readlines()]
            with open(path.join(root, filename), "w") as f:
                f.writelines(lines)

    files_changed = [emulator_name, emulator_dir]

    return list(set(files_changed))


def create_emulator(device_info):
    """
    Creates a vanilla emulator in the DeviceEmulator submodule

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        files_changed (list[Str]): List of unique files that have been changed/created
    """
    files_changed = [_add_emulator_directory_tree(device_info),
                     _replace_default_device_name(device_info)]

    return list(set(files_changed))
