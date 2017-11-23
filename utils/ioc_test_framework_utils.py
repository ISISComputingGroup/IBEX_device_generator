""" Utilities for integrating the device into the IOC test framework """
from templates.paths import TESTS_TEMPLATE
from system_paths import IOC_TEST_FRAMEWORK_ROOT
from os import path
from file_system_utils import replace_in_file, copy_file
import logging


def _add_template_test_file(device_info):
    """
    Args:
        device_info: Information for the device based on the given name
    """
    dst = device_info.ioc_test_framework_file_path()
    logging.info("Copying template ioc test framework tests to {}".format(dst))
    copy_file(TESTS_TEMPLATE, dst)

    replace_in_file(dst, [("_DEVICE_", device_info.ioc_name()),
                          ("_Device_", device_info.test_class_identifier()),
                          ("_device_", device_info.emulator_name())])


def _add_to_run_all_tests(device_info):
    """
    Args:
        device_info: Information for the device based on the given name
    """
    run_all_tests_src = path.join(IOC_TEST_FRAMEWORK_ROOT, "run_all_tests.bat")

    separator = "echo ---------------------------------------"
    case_separator = "echo;"
    title_format = "echo TESTING {} {} Sim"
    rec_sim_call_format = "call %PYTHON% \"%EPICS_KIT_ROOT%\\support\\IocTestFramework\\master\\run_tests.py\"" \
                          " -r -pf %MYPVPREFIX%  -d {0} -p %EPICS_KIT_ROOT%\\ioc\\master\\{1}\\iocBoot\\ioc{1}-IOC-01"
    dev_sim_call_format = "call %PYTHON% \"%EPICS_KIT_ROOT%\\support\\IocTestFramework\\master\\run_tests.py\"" \
                          " -pf %MYPVPREFIX% -d {0} -p %EPICS_KIT_ROOT%\\ioc\\master\\{1}\\iocBoot\ioc{1}-IOC-01 -e " \
                          "%PYTHONDIR%\\Scripts -ea %EPICS_KIT_ROOT%\\support\\DeviceEmulator\\master " \
                          "-ek lewis_emulators"
    blank = ""

    with open(run_all_tests_src, "a") as f:
        for case in [("Dev", dev_sim_call_format), ("Rec", rec_sim_call_format)]:
            lines = [blank,
                     separator,
                     title_format.format(device_info.ioc_name(), case[0]),
                     case[1].format(device_info.emulator_name(), device_info.ioc_name()),
                     separator,
                     case_separator]
            linesep = "\n"
            f.writelines([l+linesep for l in lines])


def create_test_framework(device_info):
    """
    Creates a vanilla integration of the device into the IOC test framework

    Args:
        device_info: Name-based information about the device
    """
    _add_to_run_all_tests(device_info)
    _add_template_test_file(device_info)
