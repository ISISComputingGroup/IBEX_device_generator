""" Utilities for integrating the device into the IOC test framework """
from templates.paths import TESTS_TEMPLATE, TESTS_RUN_SCRIPT
from utils.file_system_utils import replace_in_file, copy_file, mkdir, touch
import logging


def _add_template_test_file(device_info):
    """
    Args:
        device_info: Information for the device based on the given name
    """
    dst = device_info.ioc_test_framework_file_path()
    logging.info("Copying template ioc test framework tests to {}".format(dst))
    mkdir(device_info.system_tests_folder_path())
    mkdir(device_info.ioc_test_framework_folder_path())
    try:
        copy_file(TESTS_RUN_SCRIPT, device_info.ioc_test_framework_run_script_path())
    except OSError:
        pass # Carry on if file already exists
    try:
        copy_file(TESTS_TEMPLATE, dst)
    except OSError:
        pass # Carry on if file already exists
    touch(device_info.ioc_test_framework_folder_path(), "__init__.py")

    replace_in_file(dst, [("_DEVICE_", device_info.ioc_name),
                          ("_Device_", device_info.test_class_identifier()),
                          ("_device_", device_info.emulator_name())])


def create_test_framework(device_info):
    """
    Creates a vanilla integration of the device into the IOC test framework

    Args:
        device_info: Name-based information about the device
    """
    _add_template_test_file(device_info)
