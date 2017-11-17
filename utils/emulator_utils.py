""" Utilities for adding a template emulator for a new IBEX device"""
from common_utils import create_component
from system_paths import CLIENT
from templates.paths import BLANK_OPI
from system_paths import OPI_RESOURCES
from shutil import copyfile
from os import path
from lxml import etree
from logging_utils import logger

LOGGER = logger("Emulators")

def _copy_files(device):
    """
    :param device: Name of the device
    """


def create_emulator(device):
    """
    Creates a vanilla emulator in the DeviceEmulator submodule
    :param device: Name of the device to create the emulator for
    """
    _copy_files(device)
    _replace_default_name(device)
    dst = path.join(OPI_RESOURCES, _get_opi_file_name(name))
    LOGGER.info("Copying template OPI file to {}".format(dst))
    copyfile(BLANK_OPI, dst)