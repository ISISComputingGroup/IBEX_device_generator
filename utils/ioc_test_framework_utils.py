""" Utilities for integrating the device into the IOC test framework """
from templates.paths import TEMPLATE_TESTS
from system_paths import IOC_TEST_FRAMEWORK_ROOT
from shutil import copyfile
from os import path
from common_utils import replace_in_file
import logging


def _add_template_test_file(device):
    """
    :param device: Name of the device
    """
    dst = path.join(IOC_TEST_FRAMEWORK_ROOT, "tests", "{}.py".format(device))
    logging.info("Copying template ioc test framework tests to {}".format(dst))
    if path.exists(dst):
        raise RuntimeError("Unable to create template tests in {}, file already exists".format(dst))
    copyfile(TEMPLATE_TESTS, dst)

    replace_in_file(dst, [("_DEVICE_", device.upper()), ("_Device_", device.title()), ("_device_", device.lower())])


def _add_to_run_all_tests(device):
    """
    :param device: Name of the device
    """
    run_all_tests_src = path.join(IOC_TEST_FRAMEWORK_ROOT, "run_all_tests.bat")
    ioc_device_name = device.upper()
    emulator_device_name = device.lower()

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
                     title_format.format(ioc_device_name, case[0]),
                     case[1].format(emulator_device_name, ioc_device_name),
                     separator,
                     case_separator]
            unix_linesep = "\r"  # check in Unix line endings
            f.writelines([l+unix_linesep for l in lines])


def create_test_framework(device):
    """
    Creates a vanilla integration of the device into the IOC test framework
    :param device: Name of the device to create the emulator for
    """
    _add_to_run_all_tests(device)
    _add_template_test_file(device)
