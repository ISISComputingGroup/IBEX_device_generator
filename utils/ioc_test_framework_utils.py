""" Utilities for integrating the device into the IOC test framework """
from templates.paths import TESTS_TEMPLATE, TESTS_RUN_SCRIPT
from utils.file_system_utils import replace_in_file, copy_file, mkdir, touch
import logging


def _add_template_test_file(device_info, unique_name):
    """
    Args:
        device_info: Information for the device based on the given name
    """
    if unique_name.ioc_name() == "NONE":
        unique_name = device_info

    dst = unique_name.ioc_test_framework_file_path()
    logging.info("Copying template ioc test framework tests to {}".format(dst))
    mkdir(unique_name.system_tests_folder_path())
    mkdir(unique_name.ioc_test_framework_folder_path())
    copy_file(TESTS_RUN_SCRIPT, unique_name.ioc_test_framework_run_script_path())
    copy_file(TESTS_TEMPLATE, dst)
    touch(unique_name.ioc_test_framework_folder_path(), "__init__.py")

    replace_in_file(dst, [("_DEVICE_", device_info.ioc_name()),
                          ("_Device_", device_info.test_class_identifier()),
                          ("_device_", unique_name.emulator_name())])


def create_test_framework(device_info, unique_name):
    """
    Creates a vanilla integration of the device into the IOC test framework

    Args:
        device_info: Name-based information about the device
    """
    _add_template_test_file(device_info, unique_name)
