""" Utilities for integrating the device into the IOC test framework """
from templates.paths import TESTS_TEMPLATE
from system_paths import IOC_TEST_FRAMEWORK_ROOT
from os import path
from file_system_utils import replace_in_file, copy_file
import logging


def _create_template_test_file(device_info):
    """
    Copy the template test file and replace the default device names

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        directory (Str): Target directory files were copied to
    """
    directory = device_info.ioc_test_framework_file_path()
    logging.info("Copying template ioc test framework tests to {}".format(directory))
    copy_file(TESTS_TEMPLATE, directory)

    replace_in_file(directory, [("_DEVICE_", device_info.ioc_name()),
                                ("_Device_", device_info.test_class_identifier()),
                                ("_device_", device_info.emulator_name())])

    return directory


def create_test_framework(device_info):
    """
    Creates the devices basic IOC test framework test file

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        files_changed (list[Str]): List of unique files that have been changed/created
    """
    files_changed = [_create_template_test_file(device_info)]

    return list(set(files_changed))
